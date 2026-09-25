# Resolução de Coreferência.

> "Ela ligou-lhe, ele não respondeu, o médico estava no almoço". Três referências a duas pessoas e ninguém é nomeado.
> "Ela chamou-o, ele não respondeu, o médico estava no almoço".

> **【中文解读】**A partir daí, o texto pode ser traduzido em inglês.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 06 (NER), Phase 5 · 07 (POS & Parsing) | **前置知识:** Phase 5 · 06（NER），Phase 5 · 07（POS 与解析）
**Time:** ~45 minutes | **时间:** ~45 分钟

## O problema é o problema da introdução

A resolução Coreference liga todas as expressões que se referem à mesma entidade. "Barack Obama", "o presidente", "ele", "Obama" apontam para uma pessoa. Sem ele, o seu sistema NER relata quatro entidades em vez de uma, os fragmentos do gráfico de conhecimento, e o seu resumo deixa os assuntos no meio do documento.

> Compartilhar os dados de um sistema de informação e comunicação, que é o sistema de informação e comunicação, e o sistema de informação e comunicação, que é o sistema de informação e comunicação, é o sistema de informação e comunicação que é o sistema de informação e comunicação.

> **【中文解读】**A questão que se coloca neste capítulo é: como entender e aplicar esta técnica na prática da construção.

Por que é importante em 2026: LLMs lidam com coreferência implícitamente dentro de sua janela de contexto, mas a recuperação RAG ainda precisa de resolução explícita.

> Por que é importante: LLM em cima da janela de baixo texto em que o processo de processamento é feito, mas o RAG 检索 ainda precisa de uma descomposição clara.

## O conceito central.

> **【中文解读】**Este artigo apresenta os conceitos e as bases da teoria.

**Mention detection.**Encontre todas as frases e pronomes substantivos que possam se referir a uma entidade.

> **指称检测。**找到所有可能指向实体名词短语和代词──使用 POS 标签和分析树──

**Coreference clustering.**Os grupos mencionam que se referem à mesma entidade. Classificadores de pares de menção, modelos baseados em intervalos ou abordagens neurais de ponta a ponta (Lee et al., 2017).

> **共指聚类。**O termo "disciplina" refere-se a um mesmo corpo.

> **【拓展：大语言模型的工程实践】**De GPT a ChatGPT, o campo de NLP passou por uma transição de "cada tarefa treinar um modelo" para "um modelo resolver todas as tarefas".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) é a estrutura mais popular de aplicação de IA em empresas atuais.

> **【拓展：NLP 的多语言挑战】**No mundo há mais de 7000 idiomas, mas os estudos de PNL se concentram principalmente em inglês e em uma minoria de línguas.
```figure
coref-links
```

## Construí-lo

## Construí-lo e realizei-o.

> **【中文解读】**Este é o capítulo do código do zero implementar o algoritmo central.

```python
import spacy

nlp = spacy.load("en_core_web_sm")

def resolve_coref(text):
    doc = nlp(text)
    clusters = {}
    for token in doc:
        if token.pos_ == "PRON":
            # Simple heuristic: look for nearest preceding noun
            for t in reversed(list(doc[:token.i])):
                if t.pos_ in ("NOUN", "PROPN"):
                    clusters[token.text] = t.text
                    break
    return clusters
```

> **【中文解读】**Este capítulo mostra como usar um quadro de desenvolvimento rápido para aplicar esta tecnologia.

> **【拓展：Prompt Engineering 与 LLM 应用】**A Engenharia Prometida tornou-se a habilidade central de engenheiros de PNL.

## Use-o com o framework implementado.

> **【中文解读】**Este capítulo trata-se de como o modelo será implementado para produtos disponíveis.

- **spaCy with coreferee.**Coreferência de produção para inglês. / spaCy + coreferee。英语生产共指。
- **Hugging Face span-based models.**Resolução de coreferência neural. / Abraçamento de rosto  baseado em modelo de transmissão.
- **LLM prompting.**Peça ao Mestrado em Direito a resolver as referências básicas. Boa precisão, alto custo.

## Envia-o . Produto .

Salva como`outputs/skill-coref-picker.md`- Não .

> 保存为 `outputs/skill-coref-picker.md`- Não .

```markdown
Given a text and need for entity tracking, pick coreference approach.
1. Rule-based vs neural vs LLM.
2. Language support.
3. Latency budget.
```

## Exercícios.

1. **Easy.**Implementar resolução do pronome usando tags de POS. / **简单。**Use POS 标签实现代词消解──
2. **Medium.**Avaliação do centro de estudo com base num corpus de 50 frases.**中等。**Em 50 palavras, avaliar o espaço e os participantes.
3. **Hard.**Construir um pré-processador RAG que resolva as coreferências antes de ser desmontado.**困难。**Construído em blocos pré-dessolvindo o sistema de processamento RAG.

## Termos-chave .

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Coreference（共指） | Multiple expressions referring to the same entity. / 多个表达指向同一实体。 |
| Mention（指称） | A textual reference to an entity. / 对实体的文本引用。 |
| Anaphora（回指） | Pronoun referring to an earlier noun. / 代词指向前面的名词。 |

## Mais leitura 延伸阅读

- [Lee et al. (2017). End-to-end Neural Coreference Resolution](https://arxiv.org/abs/1707.07045) a abordagem baseada em span. / 基于跨度的方法──
- [coreferee](https://github.com/explosion/coreferee) spaCy coreference plugin. / spaCy 共指插件──
