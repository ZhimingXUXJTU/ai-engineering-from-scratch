# Análise de sentimentos.

> A tarefa canônica de PNL. A maior parte do que você precisa saber sobre classificação de textos clássicos aparece aqui.
> O mais clássico de NLP 任务── Classic Textbook 类中你需要知道的大部分内容都在这里──

> **【中文解读】**判断文本的情感倾向──是NLP最经典的分类任务之一── é uma das mais clássicas tarefas da PNL.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 2 · 14 (Naive Bayes) | **前置知识:** Phase 5 · 02（BoW + TF-IDF），Phase 2 · 14（朴素贝叶斯）
**Time:** ~75 minutes | **时间:** ~75 分钟

## O problema é o problema da introdução

"A comida não foi boa". Positiva ou negativa?

> "A comida não foi ótima". É verdade ou é negativa?

O sentimento soa simples. Um crítico disse que gostava ou não de algo. Etiquete a frase. A razão pela qual se tornou a tarefa canônica da PNL é que cada caso fácil de olhar esconde um difícil. A negação inverte o significado. O sarcasmo inverte-o. "Não é ruim em tudo" é positivo apesar de duas palavras codificadas negativamente. Emojis carregam mais sinal do que o texto circundante.`tight`em revisão musical versus `tight`em revisão da moda).

> O analise emocional parece simples. O comentador disse que gosta ou não gosta de nada. O seu significado é que cada caso parece ser um exemplo de NLP, mas o seu significado é muito diferente.`tight`Com a moda comentários `tight`)。

Sentimento é um laboratório de trabalho para a PNL clássica. Se você entender por que cada linha de base ingênua tem um modo de falha específico, você entenderá por que cada modelo mais rico foi inventado. Esta lição constrói uma linha de base Bayes ingênua a partir do zero, adiciona regressão logística e nomeia as armadilhas que tornam o sentimento de produção um problema de nível de conformidade.

> 情感分析 é o laboratório de trabalho da NLP clássica. Se você entender por que cada linha simples tem um padrão de falha específico, você já entende por que cada modelo mais rico foi inventado.

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.

O sentimento clássico é uma receita de dois passos.

> A análise emocional clássica é uma solução em dois passos.

1. **Represent.**Transforme o texto em um vetor de caracteres.
   **表示。**O texto será transformado em característico em volume.
2. **Classify.**Aplique um modelo linear (Naive Bayes, regressão logística, SVM) em exemplos rotulados.
   **分类。**Em seu modelo de etiquetação, o modelo é o modelo de linhação (SVM)

Naívo Bayes é o modelo mais estúpido que funciona, supõe que cada característica é independente dada a etiqueta.`P(word | positive)`E ...`P(word | negative)`A hipótese de independência "ingênua" é ridiculamente errada e os resultados são chocantes. A razão: com recursos de texto escassos e dados moderados, o classificador se importa com que lado cada palavra inclina mais do que quanto.

> O modelo mais simples de Bayes é o mais utilizado, mas administrativo.`P(word | positive)`和 `P(word | negative)` O teorema de probabilidade é ridículo, mas o resultado é surpreendente.

A regressão logística fixa a suposição de independência.`not good`O Bayes ingênuo não pode fazer isso para bigrams que nunca foi etiquetado.

> 逻辑归修复了独立性假设── é para cada característica de aprender um peso, incluindo o peso negativo──`not good`Como um dos componentes de dois dois tipos, o peso negativo é obtido.

> **【拓展：大语言模型的工程实践】**De GPT a ChatGPT, o campo do NLP passou por uma transição de paradigma de "cada tarefa treinar um modelo" para "um modelo resolver todas as tarefas".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) é a estrutura mais popular de aplicações de IA em empresas: fazer uma consulta de usuário antes de fazer uma consulta de documentos relacionados, e reapreciar o resultado da consulta como resposta de produção para o LLM.

> **【拓展：NLP 的多语言挑战】**No mundo todo, há mais de 7000 idiomas, mas os estudos de PNL se concentram principalmente em inglês e outras línguas.

## Construí-lo e realizei-o.

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.
```figure
sentiment-logits
```

## Construí-lo

### Passo 1: um mini-conjunto de dados real

```python
POSITIVE = [
    "absolutely loved this movie",
    "beautiful cinematography and a great story",
    "one of the best films of the year",
    "brilliant acting from the lead",
    "heartwarming and funny",
]

NEGATIVE = [
    "boring and far too long",
    "not worth your time",
    "the plot made no sense",
    "terrible acting, awful script",
    "i want my two hours back",
]
```

O trabalho real usa dezenas de milhares de exemplos (IMDb, SST-2, polaridade Yelp).

> Por isso, o que eu quero fazer é muito pequeno.

### Passo 2: Naívo Bayes multinomial do zero

```python
import math
from collections import Counter


def train_nb(docs_by_class, vocab, alpha=1.0):
    class_priors = {}
    class_word_probs = {}
    total_docs = sum(len(d) for d in docs_by_class.values())

    for cls, docs in docs_by_class.items():
        class_priors[cls] = len(docs) / total_docs
        counts = Counter()
        for doc in docs:
            for token in doc:
                counts[token] += 1
        total = sum(counts.values()) + alpha * len(vocab)
        class_word_probs[cls] = {
            w: (counts[w] + alpha) / total for w in vocab
        }
    return class_priors, class_word_probs


def predict_nb(doc, class_priors, class_word_probs):
    scores = {}
    for cls in class_priors:
        s = math.log(class_priors[cls])
        for token in doc:
            if token in class_word_probs[cls]:
                s += math.log(class_word_probs[cls][token])
        scores[cls] = s
    return max(scores, key=scores.get)
```

O suavização aditiva (alfa=1.0) é o suavização de Laplace. Sem ele, uma palavra invisível em uma classe tem probabilidade zero e o log explode. `alpha=0.01`É comum na prática. `alpha=1.0`é o padrão de ensino.

> 加法平滑(alpha=1.0) é 拉普拉斯平滑──没有它,一个类别中未见的词概率为零,log会爆炸──实践中 `alpha=0.01`É muito comum.`alpha=1.0`É o que é o ensino.

### Passo 3: Regressão logística a partir do zero

```python
import numpy as np


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -20, 20)))


def train_lr(X, y, epochs=500, lr=0.05, l2=0.01):
    n_features = X.shape[1]
    w = np.zeros(n_features)
    b = 0.0
    for _ in range(epochs):
        logits = X @ w + b
        preds = sigmoid(logits)
        err = preds - y
        grad_w = X.T @ err / len(y) + l2 * w
        grad_b = err.mean()
        w -= lr * grad_w
        b -= lr * grad_b
    return w, b


def predict_lr(X, w, b):
    return (sigmoid(X @ w + b) >= 0.5).astype(int)
```

A regularização L2 é importante aqui. As características do texto são escassas; sem L2 o modelo memoriza exemplos de treinamento.`0.01`e sintonizar.

> L2 normalização aqui é muito importante.`0.01`Começa a fazer.

### Passo 4: negação de manuseio (modo de falha)

Considere "não bom" e "não ruim".`{not, good}`E ...`{not, bad}`E aprende com quem mais apareceu no treinamento.`not_good`E ...`not_bad`E, por vezes, é suficiente.

> 考虑 "no bom" 和 "no mau"──BoW 分类器看 `{not, good}`和 `{not, bad}`, de acordo com o que surge no treino mais para aprender.`not_good`和 `not_bad`Como diferentes características de aprendizagem.

Uma solução mais crudíssima que funciona quando não há bigramas:**negation scoping**. Prefixo de tokens após uma palavra de negação com `NOT_`Até à próxima pontuação.

> Uma mais grosseira, mas efetiva em sem 2o grupo:**否定范围标记**                                                                                                                                                                                                                                                              `NOT_`Antes, até o próximo símbolo.

```python
NEGATION_WORDS = {"not", "no", "never", "nor", "none", "nothing", "neither"}
NEGATION_TERMINATORS = {".", "!", "?", ",", ";"}


def apply_negation(tokens):
    out = []
    negate = False
    for token in tokens:
        if token in NEGATION_TERMINATORS:
            negate = False
            out.append(token)
            continue
        if token in NEGATION_WORDS:
            negate = True
            out.append(token)
            continue
        out.append(f"NOT_{token}" if negate else token)
    return out
```

```python
>>> apply_negation(["not", "good", "at", "all", ".", "but", "funny"])
['not', 'NOT_good', 'NOT_at', 'NOT_all', '.', 'but', 'funny']
```

Agora .`good`E ...`NOT_good`O classificador pode pesá-los em oposição. três linhas de pré-processamento, precisão mensurável saltar em referência de sentimento.

> Agora , agora .`good`和 `NOT_good`As características diferentes. Os classificadores podem dar-lhes o peso oposto.

### Passo 5: métricas de avaliação que importam

A precisão por si só é enganosa se as classes são desequilibradas. Os corpos de sentimento reais são geralmente de 70-80% positivo ou 70-80% negativo; um classificador de maioria constante obtém 80% de precisão e é inútil.

> Se a classificação não for equilibrada, apenas a taxa de precisão produzirá errores. O material de expressão emocional real geralmente é de 70-80% positivo ou de 70-80% negativo. Uma maioria constante de categorias pode obter uma taxa de precisão de 80%, mas não tem valor.

- **Per-class precision and recall.**Um par por classe, uma média macro para obter um único número que respeite o equilíbrio de classe.
  **每类精确率和召回率。**Cada classe é um par.
- **Macro-F1 (primary metric for imbalanced data).**Mediano de pontuações por classe, igual a peso.
  **Macro-F1（不平衡数据的主要指标）。**O valor médio de cada classe F1 é igual ao peso.
- **Weighted-F1 (alternative).**O mesmo que o macro, mas ponderado pela frequência da classe.
  **Weighted-F1（替代方案）。**Quando não se equilibra em si tem significado comercial, com o relatório de Macro-F1
- **Confusion matrix.**Contas crudas. Inspecte sempre antes de confiar em qualquer métrica escalar; revela quais pares de classes o modelo confunde.
  **混淆矩阵。**O primeiro estudo foi realizado em 18 de janeiro de 2005 e foi publicado em 18 de janeiro de 2009.
- **Per-class error samples.**Leia cinco previsões erradas por aula, nada substitui a leitura dos erros reais.
  **每类错误样本。**Cada categoria extrai 5 erros de previsão.

Para dados gravemente desequilibrados (> 95-5 ratio), relatório **AUROC**E ...**AUPRC**O AUPRC é mais sensível à classe minoritária, que é o que normalmente se preocupa (spam, fraude, sentimento raro).

> 对于严重不平衡的数据 ((> 95-5 比例), relatório **AUROC**和 **AUPRC**A UPRC é mais sensível à minoria, isso é geralmente o que você se preocupa com os "juntos" (http://www.jsp.com/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/jsp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp/sp////sp/sp////sp/sp//////////////////////////////////////////

**Common bug to avoid.**Relatório de micro-F1 em vez de macro-F1 em dados desequilibrados dá um número que parece alto porque é dominado pela classe majoritária.

> **常见错误。**Em dados desequilibrados, o relatório Micro-F1 em vez de Macro-F1 dará um número que parece muito alto, porque é dominado pela maioria das classes.

```python
def evaluate(y_true, y_pred):
    tp = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 1)
    fp = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 1)
    fn = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 0)
    tn = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 0)
    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0
    return {"tp": tp, "fp": fp, "tn": tn, "fn": fn, "precision": precision, "recall": recall, "f1": f1}
```

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.

> **【拓展：Prompt Engineering 与 LLM 应用】**A Engenharia Prometida tornou-se a habilidade central dos engenheiros de PNL. De zero-shot a poucos-shot, de cadeia de pensamento a reação, diferentes estratégias de orientação são aplicadas a diferentes cenários.

## Use-o com o framework implementado.

O Scikit-Learn faz isto em seis linhas, corretamente.

> Aprenda a fazer isso, e é verdade.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

pipe = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True, stop_words=None)),
    ("clf", LogisticRegression(C=1.0, max_iter=1000)),
])
pipe.fit(X_train, y_train)
print(pipe.score(X_test, y_test))
```

Três coisas a notar.`stop_words=None`mantém as negações. `ngram_range=(1, 2)`Adiciona bigrams assim `not_good`torna-se uma característica. `sublinear_tf=True`Estes três sinais representam a diferença entre uma linha de base com 75% de precisão e uma linha de base com 85% de precisão na SST-2.

> Três pontos que vale a pena notar.`stop_words=None`Não quero que me deixes.`ngram_range=(1, 2)`添加二元组使 `not_good`成为特征──`sublinear_tf=True`抑制重复词── Estes três sinais são a diferença entre a linha de 75% da taxa de precisão da SST-2 e a linha de 85% da taxa de precisão da SST-2.

### Quando procurar um transformador

- Detecção de sarcasmo, os modelos clássicos falham aqui.
  O modelo clássico aqui vai falhar.
- Longas revisões onde o sentimento muda no meio do documento.
  情感在文档中转变的长评论──
- Sentimento baseado em aspectos. "A câmera era ótima, mas a bateria era terrível".
  Baseado em análise de emoção em aspectos. "A câmera era ótima, mas a bateria era terrível".
- Línguas não inglesas, de baixo recurso. O BERT multilingue dá-lhe uma linha de base de zero-shot gratuitamente.
  Não Inglês, baixo recurso linguístico, vários idiomas BERT para você gratuitamente fornecer zero modelos de linha.

Se você precisar de qualquer um dos acima, vá para a fase 7 (mergulho profundo dos transformadores). caso contrário, o Naive Bayes ou regressão logística no TF-IDF mais bigrams mais manipulação de negação é a sua linha de base de produção de 2026.

> Se você precisar de qualquer coisa, salte para a Fase 7 (Transformer Deeping)

### A armadilha da reproducibilidade (novamente)

Re-treinar modelos de sentimento é rotina. Re-avaliação não é. Números de precisão relatados em papéis usam divisões específicas, pré-processamento específico, tokenizers específicos. Se você comparar seu novo modelo com uma linha de base sem usar o mesmo pipeline, você obterá deltas enganosas. Sempre regenerar a linha de base em seu pipeline, não o número do papel.

> O novo modelo de treinamento emocional é uma operação habitual. Reavaliação não é. A taxa de precisão do relatório no artigo é de números usando uma divisão de dados específica, um determinado pré-processamento, um determinado grupo de palavras. Se você não usar o mesmo fluxo de dados para comparar o novo modelo com o fluxo de dados, você terá um diferencial de erro.

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.

## Envia-o . Produto .

Salva como`outputs/prompt-sentiment-baseline.md`- Não .

```markdown
---
name: sentiment-baseline
description: Design a sentiment analysis baseline for a new dataset.
phase: 5
lesson: 05
---

Given a dataset description (domain, language, size, label granularity, latency budget), you output:

1. Feature extraction recipe. Specify tokenizer, n-gram range, stopword policy (usually keep), negation handling (scoped prefix or bigrams).
2. Classifier. Naive Bayes for baseline, logistic regression for production, transformer only if the domain needs sarcasm / aspects / cross-lingual.
3. Evaluation plan. Report precision, recall, F1, confusion matrix, and per-class error samples (not just scalars).
4. One failure mode to monitor post-deployment. Domain drift and sarcasm are the top two.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。

Refuse to recommend dropping stopwords for sentiment tasks. Refuse to report accuracy as the sole metric when classes are imbalanced (e.g., 90% positive). Flag subword-rich languages as needing FastText or transformer embeddings over word-level TF-IDF.
```

## Exercícios.

1. **Easy.**Adicionar`apply_negation`como um passo de pré-processamento no pipeline de aprendizagem de scikit e medir o delta da F1 em um pequeno conjunto de dados de sentimento.
   **简单。**- Não .`apply_negation`Como um pre-processamento de passos adicionados a um pouco de aprendizagem 流水线, em um pequeno conjunto de dados de emoção, a medida F1 变化──
2. **Medium.**Implementar regressão logística ponderada por classe (passar `class_weight="balanced"`Mas, como é possível, a diferença entre os níveis de gravidade e os níveis de gravidade é que os níveis de gravidade são mais elevados.
   **中等。**实现类别加权逻辑回归(传递 `class_weight="balanced"`给小学学习,或自导梯度) ⋅                                                                                                                                                                                                                                                        
3. **Hard.**Construir um detector de sarcasmo treinando um segundo classificador sobre os resíduos do modelo de sentimento. Documentar a sua configuração experimental. Avise o leitor quando a sua precisão é abaixo do acaso (nível de chance em sarcasmo de 2 classes é de ~ 50% e a maioria das primeiras tentativas aterrissam lá).
   **困难。**Treinar sobre o residuo do modelo emocional para construir um teste de pulso. Registrar a configuração do seu experimento. Quando a sua precisão for inferior ao nível de pulso, adverte o leitor.

> **【中文解读】**Practicação de temas de fácil/médio/difícil  3o dificuldade de passagem  Recomendação de completar pelo menos Praça de nível médio Classe difícil  Adaptação a pesquisa profunda ou preparação para o encontro 

## Termos-chave .

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| Polarity | Positive or negative | Binary label; sometimes extended to neutral or fine-grained (5-star). | 极性（Polarity） | 正面或负面 | 二分类标签；有时扩展到中性或细粒度（5 星）。 |
| Aspect-based sentiment | Per-aspect polarity | Attribute sentiment to specific entities or attributes mentioned in text. | 基于方面的情感分析 | 每个方面的极性 | 将情感归因到文本中提到的特定实体或属性。 |
| Negation scoping | Reversing nearby tokens | Prefix tokens after "not" with `NOT_` until punctuation. | 否定范围标记 | 反转附近的 token | 在 "not" 后给 token 加 `NOT_` 前缀直到标点符号。 |
| Laplace smoothing | Adding 1 to counts | Prevents zero-probability features in Naive Bayes. | 拉普拉斯平滑 | 给计数加 1 | 防止朴素贝叶斯中出现零概率特征。 |
| L2 regularization | Shrinking weights | Adds `lambda * sum(w^2)` to loss. Essential for sparse text features. | L2 正则化 | 缩小权重 | 在损失中添加 `lambda * sum(w^2)`。对稀疏文本特征必不可少。 |

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──

## Mais leitura 延伸阅读

- [Pang and Lee (2008). Opinion Mining and Sentiment Analysis](https://www.cs.cornell.edu/home/llee/opinion-mining-sentiment-analysis-survey.html) a pesquisa fundamental. Longo, mas as primeiras quatro seções cobrem tudo clássico.
- [Wang and Manning (2012). Baselines and Bigrams: Simple, Good Sentiment and Topic Classification](https://aclanthology.org/P12-2018/) o papel que mostrou Bigrams + Naive Bayes é difícil de vencer em texto curto. / 证明二元组 + 朴素贝叶斯在短文本上难以被超越的论文──
- [scikit-learn text feature extraction docs](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction) referência para `CountVectorizer`- Não .`TfidfVectorizer`, e cada botão que sintonizar.`CountVectorizer`- Não.`TfidfVectorizer`及你将调参的每个参数的参考──
