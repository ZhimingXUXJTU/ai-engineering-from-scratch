# Inferência em Língua Natural  Envolvimento textual   文本含

> "t implica h" significa uma leitura humana t concluiria h é verdade. NLI é a tarefa de prever implicação / contradição / neutralidade.
> "t 含 h" significa humana read t 后会推断 h 为真──NLI é pré测含/矛盾/中性的任务──表面无聊,生产中承重──

> **【中文解读】**NLI 判断两个句子之间的逻辑关系: 含、矛盾、中性──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 05 (Sentiment Analysis), Phase 5 · 10 (Attention) | **前置知识:** Phase 5 · 05（情感分析），Phase 5 · 10（注意力机制）
**Time:** ~45 minutes | **时间:** ~45 分钟

## O problema é o problema da introdução

Você construiu um chatbot. Ele respondeu "sim". Como você sabe que "sim" é apoiado pelas evidências? Você precisa classificar 10.000 artigos de notícias por tópico. Você tem 50 exemplos rotulados. Você transforma em NLI: "este artigo é sobre {tópico}"  implicação ou contradição? Você precisa verificar se um resumo gerado é fiel à fonte. NLI novamente.

> Você construiu um chatbot. O que você sabe? Você sabe que o "sim" tem evidências? Você precisa de um subjetivo dividido em 10.000 artigos de notícias. Você tem 50 exemplos de marcas. Você vai traduzir para NLI:

> **【中文解读】**A questão que se coloca neste capítulo é: como entender e aplicar esta tecnologia de forma correta na engenharia real.

Os três problemas reduzem-se à Inferência de Língua Natural. NLI é a tarefa espinha dorsal que suporta a verificação de fatos, classificação de tiros zero, avaliação de resumo e verificação de recuperação.

> Estes três problemas são resumidos em teoria da linguagem natural. A NLI é a tarefa de base da verificação de fatos, da análise de amostras, da avaliação de resumos e da verificação de exames.

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.

**The task.**Dado o princípio .`t`e hipótese.`h`, classificam a sua relação como uma das seguintes: Entra em relação (t implica h), Contradição (t contradiz h), Neutral (nenhum).

> **任务。**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `t`和假设 `h`,将它们的关系分类为: 含含含 h) 矛盾t 矛盾 h) 中性都不是) ∼三分类──

**Cross-encoder approach.**Concatenate t e h, alimenta através de um transformador, classifica. Usado para aplicações críticas à precisão. Lento porque você executa o modelo completo para cada par.

> **交叉编码器方法。**拼接 t 和 h,通过 Transformer,分类──用于准确率关键的应用──慢因为每对运行完整模型──

**Bi-encoder approach.**Encodei t e h separadamente, compare embebimentos (similitude de cosina).

> **双编码器方法。**分别编码 t 和 h,比较嵌入 (弦相似度) ⋅检索快但不太准确──

> **【拓展：大语言模型的工程实践】**De GPT a ChatGPT, o campo do NLP passou por uma transição de paradigma de "cada tarefa treinar um modelo" para "um modelo resolver todas as tarefas".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) é a estrutura mais popular de aplicações de IA em empresas: fazer uma consulta de usuário antes de fazer uma consulta de documentos relacionados, e reapreciar o resultado da consulta como resposta de produção para o LLM.
```figure
nli-router
```

## Construí-lo

> **【拓展：NLP 的多语言挑战】**No mundo todo, há mais de 7000 idiomas, mas os estudos de PNL se concentram principalmente em inglês e outras línguas.

## Construí-lo e realizei-o.

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.

### Passo 1: classificação de tiros zero através da NLI

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tok = AutoTokenizer.from_pretrained("roberta-large-mnli")
model = AutoModelForSequenceClassification.from_pretrained("roberta-large-mnli")

def nli_classify(premise, hypothesis):
    inputs = tok(premise, hypothesis, return_tensors="pt", truncation=True)
    with torch.no_grad():
        logits = model(**inputs).logits[0]
    # 0=contradiction, 1=neutral, 2=entailment
    probs = torch.softmax(logits, dim=-1)
    labels = ["contradiction", "neutral", "entailment"]
    return {labels[i]: probs[i].item() for i in range(3)}

print(nli_classify("A man is playing guitar.", "Someone is making music."))
```

> **【中文解读】**Este capítulo mostra como aplicar rapidamente esta tecnologia em um quadro de experiência.

> **【拓展：Prompt Engineering 与 LLM 应用】**A Engenharia Prometida tornou-se a habilidade central dos engenheiros de PNL. De zero-shot a poucos-shot, de cadeia de pensamento a reação, diferentes estratégias de orientação são aplicadas a diferentes cenários.

## Use-o com o framework implementado.

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.

A pilha de NLI de produção:

> 生产 PNL 技术:

- **Zero-shot classification:**Modelos de NLI (DeBERTa-v3-large-mnli).
- **Fact verification:**NLI de codificação cruzada em reclamação contra evidência. / 事实验证:交叉编码器 NLI。
- **Summary faithfulness:**Verifique cada frase resumida contra a fonte. / 摘要忠实度:检查每个摘要句子与源。
- **RAG grounding:**Verificar o contexto recuperado suporta a resposta. / RAG 定:验证检索上下文支持答案──

## Envia-o . Produto .

Salva como`outputs/skill-nli-applications.md`- Não .

> 保存为 `outputs/skill-nli-applications.md`- Não .

```markdown
Given a production need (fact-checking, zero-shot classification, summary evaluation), design the NLI pipeline.
1. Model choice. Cross-encoder (accuracy) or bi-encoder (speed).
2. Input format. Premise-hypothesis pairs.
3. Evaluation. Accuracy on labeled NLI datasets.
```

> **【中文解读】**练习题按照易/中级/难三度递进;;建议至少完成中级题;;

## Exercícios.

1. **Easy.**Utilização`roberta-large-mnli`para classificação de tópicos de zero-shot em 20 frases. / **简单。**Utilização `roberta-large-mnli`Para 20 frases fazer zero sample subjetivos
2. **Medium.**Construir um verificador de fidelidade de resumo usando NLI. Avaliação na CNN/DailyMail. / **中等。**Utilize NLI 构建摘要忠诚度检查器──在 CNN/DailyMail 上评估──
3. **Hard.**Comparar o cross-encoder com o bi-encoder NLI para a verificação da resposta RAG.**困难。**Comparar o encoder de transferência com o NLI de encoder de dupla utilização para RAG  resposta de verificação.

## Termos-chave .

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| NLI（自然语言推理） | Entailment task / 蕴含任务 | Classify premise-hypothesis pairs as entailment/contradiction/neutral. / 将前提-假设对分类为蕴含/矛盾/中性。 |
| Cross-encoder（交叉编码器） | Joint encoding / 联合编码 | Encode both texts together through the full model. / 通过完整模型联合编码两个文本。 |
| Bi-encoder（双编码器） | Separate encoding / 分离编码 | Encode each text independently, compare embeddings. / 独立编码每个文本，比较嵌入。 |

## Mais leitura 延伸阅读

- [Bowman et al. (2015). SNLI](https://nlp.stanford.edu/pubs/snli_paper.pdf) o conjunto de dados da Stanford NLI. / Stanford NLI 数据集──
- [He et al. (2021). DeBERTa v3](https://arxiv.org/abs/2111.09543) Modelo NLI de última geração. / 先进 NLI 模型。
