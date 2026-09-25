# Nomeado Identificação de Entidade .

> Parece fácil até lidar com limites ambíguos, entidades aninhadas e jargão de domínio.
> Deixe-me falar de um assunto simples até encontrar um limite obscuro.

> **【中文解读】**A partir do texto, o nome de um indivíduo, o nome de um lugar, o nome de uma organização, etc. são a base da extração de informações e do esquema de conhecimento.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 03 (Word Embeddings) | **前置知识:** Phase 5 · 02（BoW + TF-IDF），Phase 5 · 03（词嵌入）
**Time:** ~75 minutes | **时间:** ~75 分钟

## O problema é o problema da introdução

"A Apple processou o Google por causa do seu acordo de pesquisa do iPhone nos EUA". Cinco entidades: Apple (ORG), Google (ORG), iPhone (PRODUCT), acordo de pesquisa (talvez), US (GPE). Um bom sistema NER extrai todos eles com tipos corretos. Um mau perde o iPhone, confunde a Apple com a Apple a empresa, e rotula "US" como PERSON.

> "A Apple processou o Google por causa do seu acordo de pesquisa do iPhone nos EUA". 五个实体:Apple(ORG)、Google(ORG)、iPhone(PRODUCTO)、search deal(可能)、US(GPE)。

O NER é o cavalo de trabalho por baixo de cada pipeline estruturada de extração. Resumo de análise, registro de conformidade, anonização de registros médicos, compreensão de consultas de busca, base para respostas de chatbot, extração de contratos legais.

> O NER é um mecanismo de trabalho para cada tipo de estratégia estruturada de estratégia de fluxo de água. Você quase não consegue ver isso, mas você sempre depende dele.

Esta lição percorre o caminho clássico (baseado em regras, HMM, CRF) para o moderno (BiLSTM-CRF, então transformadores).

> Este curso foi desenvolvido a partir de rotas clássicas (Regulamento baseado, HMM, CRF) e foi desenvolvido em direção a rotas modernas (BiLSTM-CRF, Transformer) e resolveu as limitações específicas do primeiro passo.

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.

**BIO tagging**(ou BILOU) transforma a extracção de entidades num problema de rotulagem de sequências.`B-TYPE`(inicio da entidade), `I-TYPE`(entidade interna), ou `O`(fora de qualquer entidade).

> **BIO 标注**(ou BILOU) vai ser um objeto extraído transformado em um sequência de marcas de problema.`B-TYPE`(实体开始)`I-TYPE`(não é um organismo)`O`(não está em nenhum corpo)

```
Apple    B-ORG
sued     O
Google   B-ORG
over     O
its      O
iPhone   B-PRODUCT
search   O
deal     O
in       O
the      O
US       B-GPE
.        O
```

Cadeia de entidades multi-token: `New B-GPE`- Não .`York I-GPE`- Não .`City I-GPE`Um modelo que entenda a biologia pode extrair espaços arbitrários.

> Dois símbolos:`New B-GPE`- Não.`York I-GPE`- Não.`City I-GPE`❖ compreender o modelo de BIO pode ter qualquer dimensão.

A evolução da arquitetura:

> 架构演进:

- **Rule-based.**Regex + revistas de jornal, alta precisão em entidades conhecidas, cobertura zero em novas.
  **基于规则。**正则 + 地名词典查找── para o conhecido objeto de alta precisão, para o novo objeto de zero cobertura──
- **HMM.**Modelo Markov oculto, probabilidade de emissão de um token dado, probabilidade de transição de tag para tag, decodificação Viterbi, treinado com dados rotulados.
  **HMM。**隐马尔可夫模型──给定标签的代币 发射概率,标签间转移概率──Viterbi 解码──在标签数据上训练──
- **CRF.**Campo aleatório condicional. Como HMM, mas discriminativo, para que você possa misturar características arbitrárias (forma de palavras, capitalização, palavras vizinhas). Ainda o cavalo de trabalho de produção clássico em 2026 para implementações de baixo recurso.
  **CRF。**Condições como o HMM, mas como a diferença, pode ser combinada qualquer característica (para 2026) e ainda é a principal produção do Low Resource Deployment.
- **BiLSTM-CRF.**Características neurais em vez de artesanato. LSTM lê a frase em ambas as direções, camada CRF no topo impõe sequências de tag consistentes.
  **BiLSTM-CRF。**Neuro-tráfico em vez de manual.
- **Transformer-based.**- O BERT é perfeito com uma cabeça de classificação de tokens, melhor precisão, mais computação.
  **基于 Transformer。**Use token 分类头微调 BERT──最佳准确率──最多计算量──

> **【拓展：大语言模型的工程实践】**De GPT a ChatGPT, o campo do NLP passou por uma transição de paradigma de "cada tarefa treinar um modelo" para "um modelo resolver todas as tarefas".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) é a estrutura mais popular de aplicações de IA em empresas: fazer uma consulta de usuário antes de fazer uma consulta de documentos relacionados, e reapreciar o resultado da consulta como resposta de produção para o LLM.

> **【拓展：NLP 的多语言挑战】**No mundo todo, há mais de 7000 idiomas, mas os estudos de PNL se concentram principalmente em inglês e outras línguas.

## Construí-lo e realizei-o.

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.
```figure
ner-bio-tagging
```

## Construí-lo

### Passo 1: Assistentes de etiquetado de BIO

```python
def spans_to_bio(tokens, spans):
    labels = ["O"] * len(tokens)
    for start, end, label in spans:
        labels[start] = f"B-{label}"
        for i in range(start + 1, end):
            labels[i] = f"I-{label}"
    return labels


def bio_to_spans(tokens, labels):
    spans = []
    current = None
    for i, label in enumerate(labels):
        if label.startswith("B-"):
            if current:
                spans.append(current)
            current = (i, i + 1, label[2:])
        elif label.startswith("I-") and current and current[2] == label[2:]:
            current = (current[0], i + 1, current[2])
        else:
            if current:
                spans.append(current)
                current = None
    if current:
        spans.append(current)
    return spans
```

```python
>>> tokens = ["Apple", "sued", "Google", "over", "iPhone", "sales", "."]
>>> labels = ["B-ORG", "O", "B-ORG", "O", "B-PRODUCT", "O", "O"]
>>> bio_to_spans(tokens, labels)
[(0, 1, 'ORG'), (2, 3, 'ORG'), (4, 5, 'PRODUCT')]
```

### Passo 2: Características artesanas

Para a NER clássica (não neural), as características são o jogo.

> Para o clássico, o NER, o traço é o principal.

```python
def token_features(token, prev_token, next_token):
    return {
        "lower": token.lower(),
        "is_upper": token.isupper(),
        "is_title": token.istitle(),
        "has_digit": any(c.isdigit() for c in token),
        "suffix_3": token[-3:].lower(),
        "shape": word_shape(token),
        "prev_lower": prev_token.lower() if prev_token else "<BOS>",
        "next_lower": next_token.lower() if next_token else "<EOS>",
    }


def word_shape(word):
    out = []
    for c in word:
        if c.isupper():
            out.append("X")
        elif c.islower():
            out.append("x")
        elif c.isdigit():
            out.append("d")
        else:
            out.append(c)
    return "".join(out)
```

`word_shape("iPhone")`Retorno `xXxxxx`- Não .`word_shape("USA-2024")`Retorno `XXX-dddd`Os padrões de capitalização são de alto sinal para os substantivos próprios.

> `word_shape("iPhone")` Retorno `xXxxxx`- Não.`word_shape("USA-2024")` Retorno `XXX-dddd`◊                                                                                                                                                                                                                                                              

### Passo 3: uma linha de base base baseada em regras + dicionário

```python
ORG_GAZETTEER = {"Apple", "Google", "Microsoft", "OpenAI", "Meta", "Amazon", "Netflix"}
GPE_GAZETTEER = {"US", "USA", "UK", "India", "Germany", "France"}
PRODUCT_GAZETTEER = {"iPhone", "Android", "Windows", "ChatGPT", "Claude"}


def rule_based_ner(tokens):
    labels = []
    for token in tokens:
        if token in ORG_GAZETTEER:
            labels.append("B-ORG")
        elif token in GPE_GAZETTEER:
            labels.append("B-GPE")
        elif token in PRODUCT_GAZETTEER:
            labels.append("B-PRODUCT")
        else:
            labels.append("O")
    return labels
```

Os jornais de produção têm milhões de entradas retiradas da Wikipedia e DBpedia.`Apple`A Comissão Europeia, em especial, tem de fazer uma análise dos resultados da análise da situação.

> 生产地名词典有数百万条目, 来自 Wikipedia 和 DBpedia 抓取──覆盖率不错──消歧(公司 `Apple`contra 水果 `apple`É por isso que o modelo de estatística venceu.

### Passo 4: o passo CRF (esquema, não implantes completos)

O CRF completo a partir do zero em 50 linhas não é esclarecedor sem as bases da teoria da probabilidade.`sklearn-crfsuite`Em vez disso:

>  Não é razoável utilizar o CRF completo em 50 anos desde zero sem base em probabilidade `sklearn-crfsuite`- Não .

```python
import sklearn_crfsuite

def to_features(tokens):
    out = []
    for i, tok in enumerate(tokens):
        prev = tokens[i - 1] if i > 0 else ""
        nxt = tokens[i + 1] if i + 1 < len(tokens) else ""
        out.append({
            "word.lower()": tok.lower(),
            "word.isupper()": tok.isupper(),
            "word.istitle()": tok.istitle(),
            "word.isdigit()": tok.isdigit(),
            "word.suffix3": tok[-3:].lower(),
            "word.shape": word_shape(tok),
            "prev.word.lower()": prev.lower(),
            "next.word.lower()": nxt.lower(),
            "BOS": i == 0,
            "EOS": i == len(tokens) - 1,
        })
    return out


crf = sklearn_crfsuite.CRF(algorithm="lbfgs", c1=0.1, c2=0.1, max_iterations=100, all_possible_transitions=True)
X_train = [to_features(s) for s in sentences_tokenized]
crf.fit(X_train, bio_labels_train)
```

`c1`E ...`c2`são a regularização L1 e L2. `all_possible_transitions=True`permite que o modelo aprenda sequências ilegais (por exemplo, `I-ORG`Depois`O`O CRF impõe a consistência da BIO sem que você escreva a restrição.

> `c1`和 `c2`É L1 e L2`all_possible_transitions=True`让模型学习非法序列 (por exemplo)`O`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `I-ORG`Não é muito possível, é assim que o CRF força a BIO de forma uniforme em caso de não escrever.

### Passo 5: o que adiciona um BiLSTM-CRF

As características são aprendidas. As entradas: embeddings de token (GloVe ou fastText). LSTM lê de esquerda para direita e de direita para esquerda. Os estados ocultos concatenados passam por uma camada de saída CRF. O CRF ainda impõe consistência de sequência de tag; o LSTM substitui as características artesanais por aquelas aprendidas.

> Features become learning get of──输入:token 嵌入(GloVe 或 fastText)──LSTM De esquerda para direita e de direita para esquerda 拼接的隐藏状态通过CRF 输出层──CRF 仍然强制标签序列一致性;LSTM 用到的特征替代手工特征──

```python
import torch
import torch.nn as nn


class BiLSTM_CRF_Head(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, n_labels):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, bidirectional=True, batch_first=True)
        self.fc = nn.Linear(hidden_dim * 2, n_labels)

    def forward(self, token_ids):
        e = self.embed(token_ids)
        h, _ = self.lstm(e)
        emissions = self.fc(h)
        return emissions
```

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.

Para a camada CRF, use `torchcrf.CRF`O ganho sobre o CRF feito à mão é mensurável, mas menor do que se espera, a menos que você tenha dezenas de milhares de frases rotuladas.

> CRF 层使用 `torchcrf.CRF`(Pip instalar pytorch-crf) ⋅ Em comparação com manual CRF de aumento é mensurável, mas é menor do que você espera, a menos que você tem milhares de marcas de frase ⋅

> **【拓展：Prompt Engineering 与 LLM 应用】**A Engenharia Prometida tornou-se a habilidade central dos engenheiros de PNL. De zero-shot a poucos-shot, de cadeia de pensamento a reação, diferentes estratégias de orientação são aplicadas a diferentes cenários.

## Use-o com o framework implementado.

A spaCy remete a um NER de produção fora da caixa.

> O espaço está aberto para fornecer a produção de NER.

```python
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple sued Google over its iPhone search deal in the US.")
for ent in doc.ents:
    print(f"{ent.text:20s} {ent.label_}")
```

```
Apple                ORG
Google               ORG
iPhone               ORG
US                   GPE
```

Observação`iPhone`etiquetado`ORG`Em vez de`PRODUCT`O modelo pequeno da spaCy tem uma cobertura fraca das entidades de produtos.`en_core_web_lg`O modelo de transformador (`en_core_web_trf`O que é melhor ainda.

> Atenção .`iPhone`É um sinal de`ORG`Não é`PRODUCT` espaCy de pequeno modelo sobre a cobertura do produto físico é mais fraco.`en_core_web_lg`(pior melhor, melhor)`en_core_web_trf`- É melhor.

Cara de abraço para NER baseado em BERT:

> Abraçando a Face baseado em BERT de NER:

```python
from transformers import pipeline

ner = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")
print(ner("Apple sued Google over its iPhone in the US."))
```

```
[{'entity_group': 'ORG', 'word': 'Apple', ...},
 {'entity_group': 'ORG', 'word': 'Google', ...},
 {'entity_group': 'MISC', 'word': 'iPhone', ...},
 {'entity_group': 'LOC', 'word': 'US', ...}]
```

`aggregation_strategy="simple"`Combina tokens B-X, I-X contíguos em um espaço. sem ele, você tem etiquetas de nível de token e tem que fundir-se a si mesmo.

> `aggregation_strategy="simple"`Se não tiver, você terá um token de nível, precisa de se juntar.

### NER baseado em LLM (a opção de 2026)

O LLM NER de zero e poucos tiros é agora competitivo com modelos ajustados em muitos domínios, e dramaticamente melhor quando os dados rotulados são escassos.

> O LLM NER é agora competitivo em muitos domínios com o modelo de micro-modulação, tendo maiores vantagens na escassez de dados de marcação.

- **Zero-shot prompting.**Dê ao LLM uma lista de tipos de entidades e um esquema de exemplo. Peça a saída JSON. Funciona fora da caixa; a precisão é moderada em domínios novos.
  **零样本提示。** dar ao LLM uma lista de tipos e modelos de exemplo de entidades  requer JSON 输出 开箱即用; 准确率在新领域等
- **ZeroTuneBio-style prompting.**Descompõe a tarefa em extração de candidato → significado explicação → julgamento → re-verificação. Um prompt de várias etapas (não um tiro) aumenta a precisão substancialmente no NER biomédico. O mesmo padrão funciona para domínios jurídicos, financeiros e científicos.
  **ZeroTuneBio 风格提示。**将任务分解为候选抽取 → 含义解释 → 判断 → 复查──多阶段提示(而不是一次性) na biologic medicine NER 大幅提升准确率── o mesmo modelo aplica-se ao campo da lei, finanças e ciência──
- **Dynamic prompting with RAG.**Retirar os exemplos mais similares de rotulagem de um pequeno conjunto de sementes anotadas para cada chamada de inferência; construir o prompt de poucos tiros na mosca. Em 2026 referências, isso aumenta o GPT-4 biomédico NER F1 em 11-12% sobre o prompt estático.
  **动态 RAG 提示。**Cada vez que a raciocínio é adaptado a partir de uma pequena quantidade de marcas, a análise de amostras de marcas mais semelhantes; a construção de modelos de marcas em movimento é reduzida.
- **Per-entity-type decomposition.**Para documentos longos, uma única chamada que extrai todos os tipos de entidade de uma só vez perde a recordação à medida que o comprimento aumenta. Execute um passe de extração por tipo de entidade. Custo de inferência mais alto, precisão substancialmente maior. Este é o padrão padrão para notas clínicas e contratos legais.
  **按实体类型分解。**Para o longo dos documentos, uma vez o uso é extraído de todos os tipos de entidades, com a duração aumentando a taxa de perda de convocação.

Recomendação de produção a partir de 2026: comece com uma linha de base de zero-shot LLM antes de coletar dados de treinamento.

> 2026 anos de produção recomenda: antes de recolher dados de treinamento, comece com o LLM 零样本基线.

### Onde a NER clássica ainda vence

Mesmo com LLM disponíveis, a NER clássica ganha quando:

> Mesmo tendo LLM, Classic NER em circunstâncias seguintes:

- O orçamento de latência é inferior a 50ms.
  O orçamento de atraso é inferior a 50 milímetros de segundo.
- Tens milhares de exemplos etiquetados e precisas de 98% + F1.
  Tens milhares de marcas e precisas de 98% de F1+.
- O domínio tem uma ontologia estável onde um CRF ou BiLSTM pré-treinado transfere bem.
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
- As restrições regulamentares exigem um modelo local, não gerador.
  监管约束要求本地部署的非生成式模型──

### Onde se desmorona

- **Domain shift.**O NER treinado em contratos legais tem pior desempenho do que um jornalista.
  **领域偏移。**Em CoNLL 处理法律合同时比地名词典还差──在你的领域上微调── em seu campo
- **Nested entities.**O "Bank of America Tower" é simultaneamente um ORG e uma FACILITAD. O BIO padrão não pode representar intervalos de sobreposição.
  **嵌套实体。**"Bank of America Tower" é o mesmo tempo que ORG e FASILITADE.
- **Long entities.**"Corporação Federal de Seguros de Depósitos dos Estados Unidos". Modelos de nível de tokens às vezes dividem isto.`aggregation_strategy`ou pós-processo.
  **长实体。**"Corporação Federal de Seguros de Depósitos dos Estados Unidos"." Token 级别模型有时会分分这个──使用 `aggregation_strategy`Ou depois de processado.
- **Sparse types.**Os modelos de uso geral não têm ideia, o Scispacy e o BioBERT são os pontos de partida.
  **稀疏类型。**医疗 NER 标签如 DRUG_BRAND、ADVERSE_EVENT、DOSE。通用模型一无所知──Scispacy 和 BioBERT é o ponto de partida do processo.

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.

## Envia-o . Produto .

Salva como`outputs/skill-ner-picker.md`- Não .

> 保存为 `outputs/skill-ner-picker.md`- Não .

```markdown
---
name: ner-picker
description: Pick the right NER approach for a given extraction task.
version: 1.0.0
phase: 5
lesson: 06
tags: [nlp, ner, extraction]
---

Given a task description (domain, label set, language, latency, data volume), output:

1. Approach. Rule-based + gazetteer, CRF, BiLSTM-CRF, or transformer fine-tune.
2. Starting model. Name it (spaCy model ID, Hugging Face checkpoint ID, or "custom, trained from scratch").
3. Labeling strategy. BIO, BILOU, or span-based. Justify in one sentence.
4. Evaluation. Use `seqeval`. Always report entity-level F1 (not token-level).

Refuse to recommend fine-tuning a transformer for under 500 labeled examples unless the user already has a pretrained domain model. Flag nested entities as needing span-based or multi-pass models. Require a gazetteer audit if the user mentions "production scale" and labels are unchanged from CoNLL-2003.
```

> **【中文解读】**Practicação de temas de fácil/médio/difícil  3o dificuldade de passagem  Recomendação de completar pelo menos Praça de nível médio Classe difícil  Adaptação a pesquisa profunda ou preparação para o encontro 

## Exercícios.

1. **Easy.**Implementação `bio_to_spans`(o inverso de `spans_to_bio`) e verificar a consistência de ida e volta em 10 frases.
   **简单。** realização `bio_to_spans`(`spans_to_bio`de função inversa) e em 10 个句上验证往返一致性──
2. **Medium.**Formar o CRF sklearn-crfsuite acima no conjunto de dados NER CoNLL-2003 Inglês.`seqeval`Resultado típico: ~ 84 F1.
   **中等。**Em CoNLL-2003 Inglês NER dados集上训练上述 sklearn-crfsuite CRF──使用 `seqeval`報告每类 F1──典型结果:~84 F1──
3. **Hard.**- A música é perfeita .`distilbert-base-cased`Comparar com o modelo pequeno de spaCy.
   **困难。**Em áreas específicas de NER dados`distilbert-base-cased`◊ Comparar com o espaço 小模型比较──记录数据泄漏检查并写下让你惊的地方──

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──

## Termos-chave .

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| NER（命名实体识别） | Extract names / 提取名字 | Label token spans with types (PERSON, ORG, GPE, DATE, ...). / 用类型（PERSON、ORG、GPE、DATE 等）标注 token 跨度。 |
| BIO | Tagging scheme / 标注方案 | `B-X` begins, `I-X` continues, `O` outside. / `B-X` 开始，`I-X` 继续，`O` 外部。 |
| BILOU | Better BIO / 更好的 BIO | Adds `L-X` (last), `U-X` (unit) for cleaner boundaries. / 添加 `L-X`（最后）、`U-X`（单元）以获得更清晰的边界。 |
| CRF（条件随机场） | Structured classifier / 结构化分类器 | Models transitions between labels, not just emissions. Enforces valid sequences. / 对标签间的转移建模，而不仅仅是发射。强制有效序列。 |
| Nested NER（嵌套 NER） | Overlapping entities / 重叠实体 | One span is a different entity than a sub-span of it. BIO cannot express this. / 一个跨度与其子跨度是不同的实体。BIO 无法表达这一点。 |
| Entity-level F1（实体级 F1） | Proper NER metric / 正确的 NER 指标 | Predicted span must match true span exactly. Token-level F1 overstates accuracy. / 预测跨度必须与真实跨度完全匹配。Token 级 F1 会高估准确率。 |

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.

## Mais leitura 延伸阅读

- [Lample et al. (2016). Neural Architectures for Named Entity Recognition](https://arxiv.org/abs/1603.01360) o documento BiLSTM-CRF. Canônico. / BiLSTM-CRF 论文──经典──
- [Devlin et al. (2018). BERT: Pre-training of Deep Bidirectional Transformers](https://arxiv.org/abs/1810.04805) introduz o padrão de classificação de tokens que se tornou padrão. /  introduced into becoming standard token 分类模式──
- [spaCy linguistic features — named entities](https://spacy.io/usage/linguistic-features#named-entities) referência prática para cada atributo de `Doc.ents`E ...`Span`- Não .`Doc.ents`和 `Span`Referência prática de cada um dos seus atributos:
- [seqeval](https://github.com/chakki-works/seqeval)- A biblioteca métrica correta. - Usa-a sempre.
