# PNL multilíngue PNL multilíngue

> Um modelo, mais de 100 idiomas, zero dados de treinamento para a maioria deles. A transferência translangual é o milagre prático da década de 2020.
> Um modelo, 100+ idiomas, a maioria das línguas são inúmeras.

> **【中文解读】**Modo de tratamento de várias línguas:

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 04 (GloVe, FastText, Subword), Phase 5 · 11 (Machine Translation) | **前置知识:** Phase 5 · 04（GloVe、FastText、子词），Phase 5 · 11（机器翻译）
**Time:** ~45 minutes | **时间:** ~45 分钟

## O problema é o problema da introdução

O inglês tem bilhões de exemplos rotulados. O urdu tem milhares. O maithili quase não tem nenhum. Qualquer sistema prático de NLP que atenda a um público global tem que trabalhar na longa cauda de línguas onde não existem dados de treinamento específicos de tarefas.

> Inglês tem bilhões de marcas de padrões. Urdu tem milhares.

> **【中文解读】**A questão que se coloca neste capítulo é: como entender e aplicar esta tecnologia de forma correta na engenharia real.

Os modelos multilíngues resolvem isto treinando um modelo em muitas línguas simultaneamente. A representação compartilhada permite que o modelo transfira as habilidades aprendidas em línguas de alto recurso para línguas de baixo recurso. Afinar o modelo com base na análise de sentimentos em inglês, e produz previsões surpreendentemente boas de sentimentos em Urdu fora da caixa. Isso é transferência interlingual de zero-shot, e remodelaram a forma como a PNL se transmite ao mundo.

> O modelo multilingüe, através do treinamento simultâneo de um modelo em muitas línguas, resolve esse problema. O compartilhamento de dados mostra que o modelo irá transferir as habilidades aprendidas em alto recurso para o baixo recurso. No estudo de emoções em inglês, o modelo abre-se para gerar uma previsão de emoções incríveis para a língua urdu.

Esta lição descreve as compensações, os modelos canônicos e a única decisão que faz com que as equipes que trabalham em várias línguas se sentem em dificuldade: escolher uma língua fonte para a transferência.

> Esta aula tem como nome o modelo tradicional, bem como a decisão de um grupo de trabalho em várias línguas:

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.

![Cross-lingual transfer via shared multilingual embedding space](../assets/multilingual.svg)

**Shared vocabulary.**Os modelos multilíngues usam um sentencepiece ou wordpiece tokenizer treinado em texto de todas as línguas-alvo. O vocabulário é compartilhado: a mesma unidade de subpalavras representa o mesmo morfema em todas as línguas relacionadas. `anti-`em inglês e italiano, obtém o mesmo símbolo.

> **共享词表。**Modelo de vários idiomas usado em todos os textos de idiomas-alvo para treinar SentencePiece ou WordPiece 分词器──词表是共享的:相同的子词单元在相关语言中表示相同的语素──英语和意大利语的.`anti-`Obter o mesmo token.

**Shared representation.**Um transformador treinado em modelagem de linguagem mascarada em muitas línguas aprende que frases semânticamente semelhantes em diferentes línguas produzem estados ocultos semelhantes. mBERT, XLM-R e NLLB exibem isso. Embedings para "cat" em inglês agrupam perto de "chat" em francês e "gato" em espanhol, assim como embaixamentos de frases completas.

> **共享表示。**O transformer aprendiz de diferentes idiomas em idiomas em que sentenças semelhantes são produzidas em estado oculto semelhante.

**Zero-shot transfer.**Afinal, a função de um modelo é de ajustar o modelo em dados rotulados em uma língua (geralmente inglês).

> **零样本迁移。**Em uma linguagem (normalmente inglês) os resultados linguísticos relacionados com a tipologia são fortes, mas os resultados linguísticos de distância são fracos.

**Few-shot fine-tuning.**Adicione 100-500 exemplos rotulados na língua-alvo. A precisão salta para 95-98% da linha de base inglês em tarefas de classificação. Esta é a alavanca mais econômica na PNL multilíngue.

> **少样本微调。**Na língua-alvo, adicionar 100-500 amostras de marcas. A taxa de precisão nas tarefas de classificação sobe para 95-98% da linha de base do inglês.

> **【拓展：大语言模型的工程实践】**De GPT a ChatGPT, o campo do NLP passou por uma transição de paradigma de "cada tarefa treinar um modelo" para "um modelo resolver todas as tarefas".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) é a estrutura mais popular de aplicações de IA em empresas: fazer uma consulta de usuário antes de fazer uma consulta de documentos relacionados, e reapreciar o resultado da consulta como resposta de produção para o LLM.

> **【拓展：NLP 的多语言挑战】**No mundo todo, há mais de 7000 idiomas, mas os estudos de PNL se concentram principalmente em inglês e outras línguas.

## Os modelos .

| Model / 模型 | Year / 年份 | Coverage / 覆盖 | Notes / 说明 |
|-------|------|----------|-------|
| mBERT | 2018 | 104 languages / 104 种语言 | Trained on Wikipedia. First practical multilingual LM. Weak on low-resource. / 在 Wikipedia 上训练。首个实用多语言 LM。低资源语言较弱。 |
| XLM-R | 2019 | 100 languages / 100 种语言 | Trained on CommonCrawl. Sets the cross-lingual baseline. / 在 CommonCrawl 上训练。设定跨语言基线。 |
| XLM-V | 2023 | 100 languages / 100 种语言 | XLM-R with 1M-token vocabulary. Better on low-resource. / XLM-R 配 1M token 词表。低资源更好。 |
| mT5 | 2020 | 101 languages / 101 种语言 | T5 architecture for multilingual generation. / T5 架构用于多语言生成。 |
| NLLB-200 | 2022 | 200 languages / 200 种语言 | Meta's translation model; includes 55 low-resource languages. / Meta 翻译模型；含 55 种低资源语言。 |
| BLOOM | 2022 | 46 languages + 13 programming / 46 种语言 + 13 种编程语言 | Open 176B LLM trained multilingually. / 开源 176B 多语言 LLM。 |
| Aya-23 | 2024 | 23 languages / 23 种语言 | Cohere's multilingual LLM. Strong on Arabic, Hindi, Swahili. / Cohere 多语言 LLM。阿拉伯语、印地语、斯瓦希里语强。 |

Selecione por caso de uso. Classificação funciona bem com base XLM-R como padrão sensato. tarefas geração exigem mT5 ou NLLB dependendo da tradução versus geração aberta. pares de trabalho de estilo LLM com Aya-23 ou Claude usando solicitação multilíngue explícita.

> 按用例选择──分类任务以 XLM-R-base 作为合理默认──生成任务根据翻译vs开放生成选择 mT5 或 NLLB──LLM 风格工作配合 Aya-23 或 Claude 使用显式多语言提示──

## A decisão da língua-fonte (2026 pesquisa)

A maioria das equipes utiliza o inglês como fonte de ajuste fino. Pesquisas recentes (2026) mostram que isso é muitas vezes errado.

> A maioria dos grupos de trabalho reconhece que o inglês é um idioma de fala baixa.

A semelhança linguística prevê melhor qualidade de transferência do que o tamanho do corpo bruto. Para os alvos eslavos, o alemão ou o russo geralmente vencem o inglês. Para os alvos índicos, o hindi geralmente vence o inglês.**qWALS**A métrica de similaridade (2026, baseada nos recursos do Atlas Mundial de Estruturas de Línguas) quantifica isso. **LANGRANK**(Lin et al., ACL 2019) é um método separado e anterior que classifica línguas candidatas de origem a partir de uma combinação de semelhança linguística, tamanho do corpo e parentesco genético.

> 语言相似性比原始语料大小更好地预测迁移质量──对于斯拉夫语目标,德语或俄语通常胜英语──对于印度语目标,印度语通常胜英语──**qWALS**O número de pessoas que estão em situação de doença é de aproximadamente 20 milhões.**LANGRANK**(Lin 等,ACL 2019)                                                                                                                                                                                                                                                           

Regra prática: se a sua língua-alvo tem um parente tipologicamente próximo de recursos, tente primeiro ajustar o que é, e depois compare com o inglês.

> Regra prática: se a sua língua-alvo tem um tipo de linguagem de alto recurso familiar, primeiro tente a sua sua suavização, e depois a sua comparação com a língua inglesa.

## Construí-lo e realizei-o.

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.
```figure
n5-crosslingual-bridge
```

## Construí-lo

### Passo 1: classificação interlingual de zero-shot

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tok = AutoTokenizer.from_pretrained("joeddav/xlm-roberta-large-xnli")
model = AutoModelForSequenceClassification.from_pretrained("joeddav/xlm-roberta-large-xnli")


def classify(text, candidate_labels, hypothesis_template="This text is about {}."):
    scores = {}
    for label in candidate_labels:
        hypothesis = hypothesis_template.format(label)
        inputs = tok(text, hypothesis, return_tensors="pt", truncation=True)
        with torch.no_grad():
            logits = model(**inputs).logits[0]
        entail_score = torch.softmax(logits, dim=-1)[2].item()
        scores[label] = entail_score
    return dict(sorted(scores.items(), key=lambda x: -x[1]))


print(classify("I love this product!", ["positive", "negative", "neutral"]))
print(classify("मुझे यह उत्पाद पसंद है!", ["positive", "negative", "neutral"]))
print(classify("J'adore ce produit !", ["positive", "negative", "neutral"]))
```

Um modelo, três idiomas, a mesma API. XLM-R treinado em NLI transferir dados bem para classificação através do truque de envolvimento.

> Um modelo, três idiomas, a mesma API.

### Passo 2: espaço de inserção multilingue

```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

pairs = [
    ("The cat is sleeping.", "Le chat dort."),
    ("The cat is sleeping.", "El gato está durmiendo."),
    ("The cat is sleeping.", "Die Katze schläft."),
    ("The cat is sleeping.", "The dog is barking."),
]

for eng, other in pairs:
    emb_eng = model.encode([eng], normalize_embeddings=True)[0]
    emb_other = model.encode([other], normalize_embeddings=True)[0]
    sim = float(np.dot(emb_eng, emb_other))
    print(f"  {eng!r} <-> {other!r}: cos={sim:.3f}")
```

As traduções ficam próximas no espaço de inserção. Uma frase inglesa diferente fica mais longe. É isso que faz com que a recuperação, agrupamento e semelhança interlinguários funcionem.

> 翻译在嵌入空间中距离很近. Diferentes idiomas de idiomas são mais distantes. Esta é a base do trabalho de pesquisa, aglutinação e semelhança.

### Passo 3: Estratégia de ajuste fino de poucas tiras

```python
from transformers import TrainingArguments, Trainer
from datasets import Dataset


def few_shot_finetune(base_model, base_tokenizer, examples):
    ds = Dataset.from_list(examples)

    def tokenize_fn(ex):
        out = base_tokenizer(ex["text"], truncation=True, max_length=128)
        out["labels"] = ex["label"]
        return out

    ds = ds.map(tokenize_fn)
    args = TrainingArguments(
        output_dir="out",
        per_device_train_batch_size=8,
        num_train_epochs=5,
        learning_rate=2e-5,
        save_strategy="no",
    )
    trainer = Trainer(model=base_model, args=args, train_dataset=ds)
    trainer.train()
    return base_model
```

Para 100-500 exemplos de linguagem-alvo, `num_train_epochs=5`E ...`learning_rate=2e-5`As taxas de aprendizagem mais altas causam o colapso do alinhamento multilingüe e obtém-se um modelo apenas em inglês.

>  para 100-500 个目标语言样本,`num_train_epochs=5`和 `learning_rate=2e-5`É um valor de segurança. Uma taxa de aprendizagem mais alta levará a uma queda de várias línguas, você obtém um modelo apenas em inglês.

> **【拓展：Prompt Engineering 与 LLM 应用】**A Engenharia Prometida tornou-se a habilidade central dos engenheiros de PNL. De zero-shot a poucos-shot, de cadeia de pensamento a reação, diferentes estratégias de orientação são aplicadas a diferentes cenários.

## Avaliação que realmente funciona. Avaliação realmente eficaz.

- **Per-language accuracy on held-out sets.**Não é agregado, mas o agregado esconde a cauda longa.
  **每种语言在留出集上的准确率。**Não se aglomere.
- **Benchmark against monolingual baseline.**Para línguas com dados suficientes, um modelo monolingüe treinado a partir do zero às vezes supera o multilingüe.
  **与单语基线比较。**Para linguagens com dados suficientes, o modelo de linguagem única de treinamento às vezes vence mais de um modelo de linguagem.
- **Entity-level tests.**Os modelos multilíngues geralmente têm uma tokenization fraca para scripts longe do latim.
  **实体级测试。**目標言語中的命名实体──多语言模型对远离拉丁文的书写的分词通常较弱──
- **Cross-lingual consistency.**O mesmo significado em duas línguas deve produzir a mesma previsão.
  **跨语言一致性。**两种语言中相同含义应产生相同预测――测量差距――

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.

## Use-o com o framework implementado.

A pilha de 2026:

> Tecnologia de 2026:

| Task / 任务 | Recommended / 推荐 |
|-----|-------------|
| Classification, 100 languages / 分类，100 种语言 | XLM-R-base (~270M) fine-tuned / 微调 |
| Zero-shot text classification / 零样本文本分类 | `joeddav/xlm-roberta-large-xnli` |
| Multilingual sentence embeddings / 多语言句子嵌入 | `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` |
| Translation, 200 languages / 翻译，200 种语言 | `facebook/nllb-200-distilled-600M` |
| Generative multilingual / 生成式多语言 | Claude, GPT-4, Aya-23, mT5-XXL |
| Low-resource language NLP / 低资源语言 NLP | XLM-V or domain-specific fine-tune / XLM-V 或领域微调 |

Sempre orçar para ajustar a linguagem-alvo, se o desempenho é importante.

> Se o desempenho é importante, sempre é o orçamento de pre-reserva do idioma-alvo.

### O imposto de tokenização.

Os modelos multilíngues compartilham um tokenizer em todas as suas línguas. Esse vocabulário é treinado em um corpus dominado pelo inglês, francês, espanhol, chinês, alemão. Para qualquer língua fora do conjunto dominante, três impostos compõem silenciosamente:

> O modelo multi-linguístico em todas as línguas compartilha um divisor de palavras.

- **Fertility tax.**O texto de linguagem de baixo recurso se traduz em muito mais tokens por palavra do que o inglês. Uma frase em hindi pode precisar de 3-5 vezes os tokens de uma frase em inglês equivalente.
  **繁殖税。**低资源语言文本每词分词成英语比英语多多的代币―― um indí语句子可能需要等价英语句子的3-5 倍的代币――
- **Variant recovery tax.**Cada erro de digitação, variante diacrítica, desajuste de normalização Unicode ou variação de caso se torna uma sequência de início frio não relacionada no espaço de inserção.
  **变体恢复税。**Cada erro de redação, alteração de símbolos, variações, unicode, unificação, descoincidência ou grande variação de escrita, são transformados em uma sequência de inicialização em tempo frio no espaço embutida.
- **Capacity spillover tax.**Os impostos 1 e 2 consomem posições de contexto, profundidade de camada e dimensões de incorporação.
  **容量溢出税。**税 1 和 2 消耗上下文位置、层深度和嵌入维度── deixando para o sistema de raciocínio real mais pequeno──

O sintoma prático: o seu modelo treina normalmente em hindi, a curva de perda parece correta, a perplexidade de avaliação parece razoável e os resultados da produção são sutilmente errados. **You cannot data-scale your way out of a broken tokenizer.**

> 实际症状:模型在印地语上训练正常,损失曲线正确,评估困惑度合理,但生产输出微妙地出错――**你无法通过数据扩展来修复损坏的分词器。**

Mitigations: escolha um tokenizer com boa cobertura para a sua língua-alvo; verifique a fertilidade da tokenização no texto-alvo mantido; use fallback de nível de byte para scripts verdadeiramente long-tail.

> 缓解措施:选择对目标语言覆盖良好的分词器;在留出的目标文本上验证分词繁殖率;对真正长尾书写使用字节级回归──

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.

## Envia-o . Produto .

Salva como`outputs/skill-multilingual-picker.md`- Não .

> 保存为 `outputs/skill-multilingual-picker.md`- Não .

```markdown
---
name: multilingual-picker
description: Pick source language, target model, and evaluation plan for a multilingual NLP task.
version: 1.0.0
phase: 5
lesson: 18
tags: [nlp, multilingual, cross-lingual]
---

Given requirements (target languages, task type, available labeled data per language), output:

1. Source language for fine-tuning. Default English; check LANGRANK or qWALS if target language has a typologically close high-resource language.
2. Base model. XLM-R (classification), mT5 (generation), NLLB (translation), Aya-23 (generative LLM).
3. Few-shot budget. Start with 100-500 target-language examples if available.
4. Evaluation plan. Per-language accuracy, cross-lingual consistency, entity-level F1 on non-Latin scripts.

Refuse to ship a multilingual model without per-language evaluation. Flag scripts with low tokenization coverage as needing byte-fallback.
```

> **【中文解读】**Practicação de temas de fácil/médio/difícil  3o dificuldade de passagem  Recomendação de completar pelo menos Praça de nível médio Classe difícil  Adaptação a pesquisa profunda ou preparação para o encontro 

## Exercícios.

1. **Easy.**Execute o pipeline de classificação de tiros zero em 10 frases por língua em inglês, francês, hindi e árabe.
   **简单。**Em inglês, francês, indiano e árabe, operando em zero exemplos de classes de fluxo de água, em cada língua 10 frases.
2. **Medium.**Utilização`paraphrase-multilingual-MiniLM-L12-v2`Para construir um retriever interlingual sobre um pequeno corpus de línguas mistas.
   **中等。**构建跨语言检索器──用英语查询,检索任何语言的文档──测量 recall@5──
3. **Hard.**Compare a linguagem inglesa e a linguagem hindi para uma tarefa de classificação hindi. Relate qual a fonte produz melhor precisão hindi.
   **困难。**Comparar fontes de inglês e fontes de indígenas para reduzir os efeitos das tarefas de divisão de idiomas indianos.

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──

## Termos-chave .

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Multilingual model（多语言模型） | One model, many languages / 一个模型多种语言 | Shared vocabulary and parameters across languages. / 跨语言共享词表和参数。 |
| Cross-lingual transfer（跨语言迁移） | Train on one, run on another / 训练一种，运行另一种 | Fine-tune on source, evaluate on target without target labels. / 在源语言微调，在目标语言评估。 |
| Zero-shot（零样本） | No target labels / 无目标标签 | Transfer without target-language fine-tuning. / 无目标语言微调的迁移。 |
| Few-shot（少样本） | Small target labels / 少量目标标签 | 100-500 target-language examples for fine-tuning. / 100-500 个目标语言样本。 |
| mBERT | First multilingual LM / 首个多语言 LM | 104-language BERT on Wikipedia. / 104 语言 BERT。 |
| XLM-R | Cross-lingual baseline / 跨语言基线 | 100-language RoBERTa on CommonCrawl. / 100 语言 RoBERTa。 |
| NLLB | 200-language MT / 200 语言 MT | No Language Left Behind. 55 low-resource languages. / 不让任何语言掉队。55 种低资源语言。 |

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.

## Mais leitura 延伸阅读

- [Conneau et al. (2019). XLM-R](https://arxiv.org/abs/1911.02116)O artigo XLM-R.
- [Pires et al. (2019). How Multilingual is Multilingual BERT?](https://arxiv.org/abs/1906.01502) análise de transferência translangual. / 跨语言迁移分析。
- [Costa-jussà et al. (2022). No Language Left Behind](https://arxiv.org/abs/2207.04672) NLLB-200. / NLLB-200 论文。
- [Üstün et al. (2024). Aya Model](https://arxiv.org/abs/2402.07827) LLM multilingue da Cohere.
- [Language Similarity Predicts Cross-Lingual Transfer (2026)](https://www.mdpi.com/2504-4990/8/3/65) QWALS / LANGRANK. / QWALS / LANGRANK 源语言论文。
