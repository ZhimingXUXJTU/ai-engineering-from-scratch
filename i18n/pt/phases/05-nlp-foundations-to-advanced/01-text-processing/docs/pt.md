# Processamento de texto Tokenization, Stemming, Lemmatization, 文本处理 分词、词干提取、词形還原

> A linguagem é contínua, os modelos são discretos, o pré-processamento é a ponte.
> O modelo é separado. O pre-processamento é um ponte entre os dois.

> **【中文解读】**分词是 NLP's first step:把连续文本切成离散 token──包括词干提取和词形回原──在 LLM 时代,分词由 BPE 等子词分词器处理──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 2 · 14 (Naive Bayes) | **前置知识:** Phase 2 · 14（朴素贝叶斯）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Objetivos de aprendizagem

- Entender a tokenization, stemming e lemmatization como operações de pré-processamento distintas
  compreender分词、词干提取和词形还原 como diferentes operações de pré-processamento
- Construa um tokenizer regex, um passo de Porter voters e um lemmatizer baseado em busca a partir do zero
  Desde zero construção de regras de divisão de palavras ‧Porter 词干提取步骤和基于查找表的词形回原器
- Compare NLTK e spaCy para as tuberícias de pré-processamento de produção
  Comparar NLTK e espaCy na produção pré-processamento fluxo de água
- Reconhecer as duas falhas de produção mais comuns: deriva de reprodução e desajuste de trens/inferência
  Identificação dos dois tipos mais comuns de falhas de produção:

## O problema é o problema da introdução

Um modelo não pode ler "Os gatos estavam a correr".

> 模型不能直接读取 "Os gatos estavam correndo".

Cada sistema de PNL abre com as mesmas três perguntas: onde começa uma palavra? qual é a raiz da palavra? como tratamos "correr", "correr", "correr" como a mesma coisa quando ajuda e como coisas diferentes quando não ajuda?

> Cada sistema de PNL tem que responder às mesmas três perguntas: um termo de onde começa? qual é a raiz do termo? como vamos "corrê" quando necessário, "corrê" quando necessário, "corrê" quando necessário, como vermos a mesma coisa, e quando não precisamos, como diferenciar?

Se o tokenizer for bem, o modelo aprende do lixo.`don't`Como um símbolo , mas`do n't`Se o voto cair, o treinamento se divide.`organization`E ...`organ`Se o lematizer precisa de um contexto de fala, mas não o passa, os verbos são tratados como substantivos.

> Se o teu aparelho de palavras estiver errado, o modelo está aprendendo com dados de lixo.`don't`Como um símbolo, mas...`do n't`Quando dois, a formação se divide. Se o teu vocabulário se divide.`organization`和 `organ`结为同一个词干,主题建模就会失效──如果你的词形还原器需要词性上下文但你没有传入,动词就会被当作名词处理──

Esta lição constrói os três passos de pré-processamento a partir do zero, e mostra como a NLTK e a spaCy fazem o mesmo trabalho para que você possa ver as compensações.

> Este curso começa com a construção de zero e mostra os três passos de pre-processamento, e depois mostra como fazer o mesmo trabalho com a NLTK e o espaço, deixando-o ver o peso entre eles.

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.

Três operações, cada uma tem um trabalho e um modo de falha.

> Três operações, cada um tem suas próprias responsabilidades e um modelo de fracasso.

**Tokenization**"Token" é deliberadamente vaga porque a granularidade certa depende da tarefa. Nível de palavra para a PNL clássica. Subpalavra para transformadores. Caracterismo para linguagens sem espaço em branco.

> **分词（Tokenization）**O termo "Token" é intencional, pois a graça adequada depende de uma tarefa específica.

**Stemming**- É rápido, agressivo, estúpido.`running -> run`- Não .`organization -> organ`O segundo é o modo de falha.

> **词干提取（Stemming）**Utilizações de regras de corte ── 快速、激进、粗暴──`running -> run`- Não.`organization -> organ`O segundo exemplo é o seu modelo de fracasso.

**Lemmatization**O método de análise de dados é o de um texto que reduz uma palavra à sua forma de dicionário utilizando conhecimentos gramaticais.`ran -> run`(necessita de saber que "run" é o tempo passado de "run"). `better -> good`(necessita de saber formas comparativas).

> **词形还原（Lemmatization）**Utilize语法知识将词还原为词典形式──较慢、准确、需要查找表或形态分析器──`ran -> run`(Necessito saber que "Run" é "Run" do passado)`better -> good`(necessário saber a forma de comparação)

Regra de ouro. Cria quando a velocidade é importante e você pode tolerar ruído (indexação de pesquisa, classificação aproximada). Lemmatize quando o significado é importante (resposta a pergunta, pesquisa semântica, qualquer coisa que o usuário leia).

> 經驗法则: quando a velocidade é importante e pode tolerar ruído, use word干提取 (searching) 搜索引、粗略分类) ―― quando a tradução é importante quando a tradução é usada (searching) 问答、语义搜索、任何用户会阅读的场景) ――

> **【拓展：大语言模型的工程实践】**De GPT a ChatGPT, o campo do NLP passou por uma transição de paradigma de "cada tarefa treinar um modelo" para "um modelo resolver todas as tarefas".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) é a estrutura mais popular de aplicações de IA em empresas: fazer uma consulta de usuário antes de fazer uma consulta de documentos relacionados, e reapreciar o resultado da consulta como resposta de produção para o LLM.

> **【拓展：NLP 的多语言挑战】**No mundo todo, há mais de 7000 idiomas, mas os estudos de PNL se concentram principalmente em inglês e outras línguas.

## Construí-lo e realizei-o.

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.
```figure
edit-distance
```

## Construí-lo

### Passo 1: um tokenizer de palavras regex

O tokenizer mais simples e útil divide-se em caracteres não alfanuméricos, mantendo a pontuação como seus próprios tokens.

> O mais simples e prático é dividir os símbolos numéricos em letras não-alfabetas, ao mesmo tempo em que os símbolos de ponto são reservados para um token independente. Não é perfeito, nem é o final, mas uma linha de código pode ser executada.

```python
import re

def tokenize(text):
    return re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?|[0-9]+|[^\sA-Za-z0-9]", text)
```

Três padrões em ordem de prioridade.`don't`- Não .`it's`Números puros: qualquer único carácter não-alfanumérico não-espacial como um símbolo independente (puntuação).

> Três palavras em ordem de prioridade`don't`- Não.`it's`)。 puro número。 qualquer único não-cabeça não-alfabeto caracteres numéricos como símbolo independente(标点符号)。

```python
>>> tokenize("The cats weren't running at 3pm.")
['The', 'cats', "weren't", 'running', 'at', '3', 'pm', '.']
```

Modos de falha para detectar. `3pm`Dividiu-se em `['3', 'pm']`porque alternamos entre corridas de letras e corridas de dígitos. É bom o suficiente para a maioria das tarefas. URLs, e-mails, hashtags todos quebram. Para produção, adicione padrões antes dos gerais.

> 需要注意的失败模式── Não é o que se passa?`3pm`Foi desfeita.`['3', 'pm']`, porque nós fizemos a troca entre a sequência de letras e a sequência de números. É bom o suficiente para a maioria das tarefas.

### Passo 2: um Porter stemmer (apenas o passo 1a)

O algoritmo completo de Porter tem cinco fases de regras.

> O algoritmo completo de Porter tem cinco fases de regras. Apenas o passo 1a abrange o mais comum do inglês, e mostra um modelo de regras.

```python
def stem_step_1a(word):
    if word.endswith("sses"):
        return word[:-2]
    if word.endswith("ies"):
        return word[:-2]
    if word.endswith("ss"):
        return word
    if word.endswith("s") and len(word) > 1:
        return word[:-1]
    return word
```

```python
>>> [stem_step_1a(w) for w in ["caresses", "ponies", "caress", "cats"]]
['caress', 'poni', 'caress', 'cat']
```

Leia as regras de cima para baixo.`ies -> i`A regra é por isso .`ponies -> poni`Não , não .`pony`O Porter Real tem o passo 1B que o corrigiria, as regras competem, as regras anteriores ganham, a ordem importa mais do que qualquer regra.

> Desde cima até baixo.`ies -> i`Regras são:`ponies -> poni`Não é?`pony`A verdadeira Porter algoritmo tem um passo 1b para corrigir este problema. As regras competem entre si, e as regras que estão na frente ganham.

### Passo 3: um lemmatizer baseado em busca

A lematização adequada requer morfologia. Uma versão de ensino tratável usa uma pequena tabela de lemas e um fallback.

> A verdade é que o texto é muito mais simples do que o texto.

```python
LEMMA_TABLE = {
    ("running", "VERB"): "run",
    ("ran", "VERB"): "run",
    ("runs", "VERB"): "run",
    ("better", "ADJ"): "good",
    ("best", "ADJ"): "good",
    ("cats", "NOUN"): "cat",
    ("cat", "NOUN"): "cat",
    ("were", "VERB"): "be",
    ("was", "VERB"): "be",
    ("is", "VERB"): "be",
}

def lemmatize(word, pos):
    key = (word.lower(), pos)
    if key in LEMMA_TABLE:
        return LEMMA_TABLE[key]
    if pos == "VERB" and word.endswith("ing"):
        return word[:-3]
    if pos == "NOUN" and word.endswith("s"):
        return word[:-1]
    return word.lower()
```

```python
>>> lemmatize("running", "VERB")
'run'
>>> lemmatize("cats", "NOUN")
'cat'
>>> lemmatize("better", "ADJ")
'good'
>>> lemmatize("watched", "VERB")
'watched'
```

O último caso é o momento de ensino fundamental.`watched`Não está na nossa mesa e o nosso retorno só se ocupa .`ing`- A verdadeira lematização cobre`ed`, verbos irregulares, adjetivos comparativos, plurais com alterações sonoras (`children -> child`É por isso que os sistemas de produção utilizam o WordNet, o morfologizador da spaCy, ou um analista morfológico completo.

> O último exemplo é o momento de ensino fundamental.`watched`Não está no nosso quadro, mas a nossa estratégia de reserva só se trata.`ing`◊ verdadeiro 词形还原覆盖 `ed`、不规则动词、比较级形容词、语音变化的复数(`children -> child`)― é por isso que o sistema de produção usa o analista de forma WordNet, o analista de forma completa do espaço-espaço.

### Passo 4: Enrolar-lhes

```python
def preprocess(text, pos_tagger=None):
    tokens = tokenize(text)
    stems = [stem_step_1a(t.lower()) for t in tokens]
    tags = pos_tagger(tokens) if pos_tagger else [(t, "NOUN") for t in tokens]
    lemmas = [lemmatize(word, pos) for word, pos in tags]
    return {"tokens": tokens, "stems": stems, "lemmas": lemmas}
```

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.

A peça que falta é um tagger POS. Fase 5 · 07 (POS Tagging) cria um. Por enquanto, tudo é padrão para `NOUN`e reconhecer a limitação.

> 缺少的部分是词性标注器──Phase 5 · 07(词性标注) vai construir uma──`NOUN`Não reconheço esta limitação.

> **【拓展：Prompt Engineering 与 LLM 应用】**A Engenharia Prometida tornou-se a habilidade central dos engenheiros de PNL. De zero-shot a poucos-shot, de cadeia de pensamento a reação, diferentes estratégias de orientação são aplicadas a diferentes cenários.

## Use-o com o framework implementado.

A NLTK e a spaCy enviam as versões de produção, algumas linhas cada.

> NLTK e espaCy forneceram uma versão de produção em classe.

### NLTK

```python
import nltk
nltk.download("punkt_tab")
nltk.download("wordnet")
nltk.download("averaged_perceptron_tagger_eng")

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk import pos_tag

text = "The cats were running."
tokens = word_tokenize(text)
stems = [PorterStemmer().stem(t) for t in tokens]
lemmatizer = WordNetLemmatizer()
tagged = pos_tag(tokens)


def nltk_pos_to_wordnet(tag):
    if tag.startswith("V"):
        return "v"
    if tag.startswith("J"):
        return "a"
    if tag.startswith("R"):
        return "r"
    return "n"


lemmas = [lemmatizer.lemmatize(t, nltk_pos_to_wordnet(tag)) for t, tag in tagged]
```

`word_tokenize`Tratam contrações, Unicode, casos de borda que o seu regex perde.`PorterStemmer`- É a primeira vez que o sistema opera.`WordNetLemmatizer`O sistema de tradução acima é o pouco que a maioria dos tutoriais esquiva.

> `word_tokenize`处理缩写、Unicode 和你的正则表达式遗漏的边界情况──`PorterStemmer`运行所有五个阶段──`WordNetLemmatizer`需要将 NLTK's Penn Treebank 词性标注方案转换为 WordNet's缩写集── 需要将 NLTK's Penn Treebank 词性标注方案转换为 WordNet's缩写集── 需要将 NLTK's Penn Treebank 词性标注方案转换为 WordNet's缩写集── 需要将 NLTK's Penn Treebank 词性标注方案转换为 WordNet's缩写集── 需要将 NLTK's Penn Treebank 词性标注方案转换为 WordNet's缩写集── 需要将 NLTK's Penn Treebank 词性标注方案转换为 WordNet's缩写集── 需要转换代码转换代码是大多数教程跳过的部分──

### Espaço

```python
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("The cats were running.")

for token in doc:
    print(token.text, token.lemma_, token.pos_)
```

```
The      the     DET
cats     cat     NOUN
were     be      AUX
running  run     VERB
.        .       PUNCT
```

O spaCy esconde o gasoduto todo atrás .`nlp(text)`A tokenization, a tagging e a lematization funcionam todos. Mais rápido que o NLTK em escala. Mais preciso fora da caixa.

> O espaço vai esconder toda a linha de fluxo de água.`nlp(text)`背后──分词、词性标注和词形还原全部运行── em grande escala, em menor velocidade que o NLTK, mais rápido, em maior precisão──代价是你无法轻松替换单个组件──

### Quando escolher qual

| Situation | Pick | 场景 | 选择 |
|-----------|------|------|------|
| Teaching, research, swapping components | NLTK | 教学、研究、需要替换组件 | NLTK |
| Production, multi-language, speed matters | spaCy | 生产环境、多语言、速度要求高 | spaCy |
| Transformer pipeline (you'll tokenize with the model's tokenizer anyway) | Use `tokenizers` / `transformers` and skip classical preprocessing | Transformer 流水线（反正你会用模型自带的分词器） | 使用 `tokenizers` / `transformers`，跳过经典预处理 |

### Os dois modos de falha ninguém te avisa

A maioria dos tutoriais ensina os algoritmos e para. Duas coisas vão morder um verdadeiro pipeline de pré-processamento, e quase nunca são cobertas.

> A maioria dos cursos de ensino de algoritmos está parado. Há duas questões que vão até a linha de tratamento real, e quase nunca são mencionadas.

**Reproducibility drift.**O NLTK e o spaCy alteram o comportamento de tokenização e lemmatizer entre as versões.`['do', "n't"]`em spaCy 2.x pode produzir `["don't"]`O seu modelo foi treinado em uma distribuição. a inferência agora corre em outra. a precisão diminui silenciosamente e ninguém sabe por quê.`requirements.txt`Escreva um teste de regressão de pré-processamento que congele a tokenization esperada de 20 frases de amostra.

> **可复现性漂移。**NLTK 和 spaCy em diferentes versões entre se alterar分詞和词形復原行為── em spaCy 2.x se produzir `['do', "n't"]`Resultados, em 3.x podem ocorrer.`["don't"]`Tossa modelo está em uma distribuição, quando se faz a ideia, quando se faz a ideia em outra distribuição Precision rate ren below, nobody knows the reason`requirements.txt`中固定库版本──写一个预处理回归测试,结 20 个样本句子的预期分词结果── cada uma das suas substituições,

**Training / inference mismatch.**Treinar com pré-processamento agressivo (minúscula, remoção de palavras-stop, estemming), implementar na entrada de usuário bruto, cratera de desempenho de relógio. Esta é a falha de produção NLP mais comum.

> **训练/推理不匹配。** quando se utiliza o pre-processamento intensivo (小写化、停用词除、词干提取), quando se implementa com o input do usuário original, observe a queda de desempenho.  é o único problema mais comum na produção de PNL. Se você fizer o pre-processamento durante o treinamento, a sugestão deve executar a mesma função.

## Envia-o . Produto .

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.

Um prompt reutilizável que ajuda os engenheiros a escolher uma estratégia de pré-processamento sem ler três livros didáticos.

> Um rápido e repetível, ajudando o engenheiro a escolher estratégias de pré-processamento sem necessidade de ler os três livros didáticos.

Salva como`outputs/prompt-preprocessing-advisor.md`- Não .

```markdown
---
name: preprocessing-advisor
description: Recommends a tokenization, stemming, and lemmatization setup for an NLP task.
phase: 5
lesson: 01
---

You advise on classical NLP preprocessing. Given a task description, you output:

1. Tokenization choice (regex, NLTK word_tokenize, spaCy, or transformer tokenizer). Explain why.
2. Whether to stem, lemmatize, both, or neither. Explain why.
3. Specific library calls. Name the functions. Quote the POS-tag translation if NLTK is involved.
4. One failure mode the user should test for.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。

Refuse to recommend stemming for user-visible text. Refuse to recommend lemmatization without POS tags. Flag non-English input as needing a different pipeline.
```

## Exercícios.

1. **Easy.**Extensão`tokenize`Para manter URLs como tokens individuais.`tokenize("Visit https://example.com today.")`deve produzir um token de URL.
   **简单。**扩展 `tokenize`Use URL 保持为单个代币──测试:`tokenize("Visit https://example.com today.")`应产生一个URL代号――
2. **Medium.**Implementar o passo Porter 1b. Se uma palavra contém uma vocala e termina em `ed`ou `ing`- Não, não, não, não.`hopping -> hop`Não , não .`hopp`)).
   **中等。**实现 Porter 步骤 1b.`ed`Ou `ing`结尾,则移除它──处理双辅音规则(`hopping -> hop`- Não .`hopp`)。
3. **Hard.**Construa um lemmatizer que use o WordNet como uma tabela de pesquisa, mas cai de volta para os seus votantes de Porter quando o WordNet não tem entrada.
   **困难。**Construir um usando WordNet  como um mecanismo de busca de palavras  quando WordNet  sem条目时回归你的波特词干提取器── em medição no material de tag em relação ao puro WordNet 和纯波特的准确率──

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──

## Termos-chave .

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| Token | A word | Whatever unit the model consumes. Can be word, subword, character, or byte. | Token（词元） | 一个词 | 模型消耗的任何单位。可以是词、子词、字符或字节。 |
| Stem | Root of a word | Result of rule-based suffix stripping. Not always a real word. | Stem（词干） | 词的词根 | 基于规则的后缀剥离结果。不一定是真正的词。 |
| Lemma | Dictionary form | The form you'd look up. Requires grammatical context to compute correctly. | Lemma（词元形式） | 词典形式 | 你会去词典中查找的形式。需要语法上下文才能正确计算。 |
| POS tag | Part of speech | Category like NOUN, VERB, ADJ. Needed to lemmatize accurately. | POS tag（词性标注） | 词性 | 如 NOUN、VERB、ADJ 等类别。准确词形还原需要它。 |
| Morphology | Word shape rules | How a word changes form based on tense, number, case. Lemmatization depends on it. | Morphology（形态学） | 词形变化规则 | 词如何根据时态、数、格变化形式。词形还原依赖它。 |

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.

## Mais leitura 延伸阅读

- [Porter, M. F. (1980). An algorithm for suffix stripping](https://tartarus.org/martin/PorterStemmer/def.txt)O artigo original, cinco páginas, ainda é a explicação mais clara.
- [spaCy 101 — linguistic features](https://spacy.io/usage/linguistic-features)Como é que um oleoduto real é conectado?
- [NLTK book, chapter 3](https://www.nltk.org/book/ch03.html) casos de margem de tokenization que ainda não pensou. / Você ainda não pensou de分词边界情况──
