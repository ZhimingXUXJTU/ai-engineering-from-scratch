# Entidade Linking & Disambiguation

> A NER encontrou "Paris". A entidade que liga decide: Paris, França? Paris Hilton? Paris, Texas? Paris (o príncipe troiano)? Sem ligar, o seu gráfico de conhecimento permanece ambíguo.
> NER 找到了 "Paris"──实体链接决定:巴黎(França?Paris·Hilton?Paris(Texas?Paris(特洛伊王子?

> **【中文解读】**O NER 提取的实体链接到知识库中的唯一条目――

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 06 (NER), Phase 5 · 22 (Embedding Models) | **前置知识:** Phase 5 · 06（NER），Phase 5 · 22（嵌入模型）
**Time:** ~45 minutes | **时间:** ~45 分钟

## O problema é o problema da introdução

A ligação de entidades (EL) resolve cada menção a uma entrada única em uma base de conhecimentos (Wikidata, Wikipedia, GeoNames).

> 实体链接(EL) vai resolver cada indicação em seu único artigo (Wikidata、Wikipedia、GeoNames)

> **【中文解读】**A questão que se coloca neste capítulo é: como entender e aplicar esta técnica na prática da construção.

## O conceito central.

> **【中文解读】**Este artigo apresenta os conceitos e as bases da teoria.

**Candidate generation.**Dado "Jordan", quais entradas KB correspondem? Use a combinação de cadeias, resolução redirecionada e pré-requisitos de popularidade.

> **候选生成。**给定 "Jordan", que informações são adequadas? use字符串匹配、重定向解析和流行度先验──通常检索前10-50个候选──

**Disambiguation.**Classificar candidatos por semelhança de contexto. Bi-encoder para velocidade, cross-encoder para precisão. Contexto = texto circundante + descrição de entidade a partir de KB.

> **消歧。**按上下文相似度排名候选──双编码器用于速度,交叉编码器用于准确率──上下文 = 周围文本 + 知识库中的实体描述──

> **【拓展：大语言模型的工程实践】**O GPT foi transformado em um campo de discussão.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) é a estrutura mais popular de aplicação de IA em empresas atuais.

> **【拓展：NLP 的多语言挑战】**No mundo há mais de 7000 idiomas, mas os estudos de PNL se concentram principalmente em inglês e em uma minoria de línguas.

## Construí-lo e realizei-o.

> **【中文解读】**Este é o capítulo do código do zero implementar o algoritmo central.
```figure
gx-entity-linking
```

## Construí-lo

### Passo 1: criar um índice de alias a partir de redirecionamentos da Wikipédia

```python
alias_to_entities = {
    "jordan": ["Q41421 (Michael Jordan)", "Q810 (Jordan, country)", "Q254110 (Michael B. Jordan)"],
    "paris":  ["Q90 (Paris, France)", "Q663094 (Paris, Texas)", "Q55411 (Paris Hilton)"],
    "apple":  ["Q312 (Apple Inc.)", "Q89 (apple, fruit)"],
}
```

Dados alias da Wikipédia: ~ 18M (alias, entidade) pares. Descarregar de depósitos de Wikidata. Armazenar como índice invertido.

### Passo 2: Desambiguação baseada no contexto

```python
def entity_link(mention, context, kb_lookup, embed_model):
    candidates = kb_lookup.get(mention.lower(), [])
    if not candidates:
        return None
    ctx_emb = embed_model.encode([context])
    scores = []
    for cand in candidates:
        cand_emb = embed_model.encode([cand["description"]])
        scores.append((cand, float(np.dot(ctx_emb[0], cand_emb[0]))))
    return max(scores, key=lambda x: x[1])[0]
```

> **【中文解读】**Este capítulo mostra como usar um quadro de desenvolvimento rápido para aplicar esta tecnologia.

> **【拓展：Prompt Engineering 与 LLM 应用】**A Engenharia Prometida tornou-se a habilidade central de engenheiros de PNL.

## Use-o com o framework implementado.

> **【中文解读】**Este capítulo trata-se de como o modelo será implementado para produtos disponíveis.

- **OpenTapioca.**EL leve para Wikidata. / OpenTapioca。Wikidata 轻量 EL。
- **REL (Radboud Entity Linker).**Estado da arte Wikipedia EL. / REL。先进 Wikipedia EL。
- **GENRE.**Autoregressiva entidade ligando por Facebook. / GENRE。Facebook 自回归实体链接。
- **LLM prompting.**Peça ao Mestrado em Direito a desambiguação.

## Envia-o . Produto .

Salva como`outputs/skill-entity-linker.md`- Não .

> 保存为 `outputs/skill-entity-linker.md`- Não .

```markdown
Given mentions from NER, link them to a knowledge base.
1. KB choice (Wikidata, Wikipedia, custom).
2. Candidate generation strategy.
3. Disambiguation method (embedding similarity, cross-encoder, LLM).
```

## Exercícios.

1. **Easy.**Construir um gerador de candidatos baseado na Wikipedia. / **简单。**构建基于维基百科的候选生成器──
2. **Medium.**Implementar desambiguação de bi-encoder e avaliar num conjunto de testes. / **中等。**实现双编码器消歧──
3. **Hard.**Comparar EL baseado em LLM com EL neural num conjunto de dados multilingüe. / **困难。**Em multilingual data collection comparar LLM EL vs 神经 EL.

## Termos-chave .

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Entity linking（实体链接） | Map mentions to KB entries. / 将指称映射到知识库条目。 |
| Disambiguation（消歧） | Pick the correct entity among candidates. / 在候选中选择正确实体。 |
| Candidate generation（候选生成） | Retrieve possible KB matches for a mention. / 为指称检索可能的知识库匹配。 |

## Mais leitura 延伸阅读

- [Wu et al. (2020). Scalable Zero-shot Entity Linking](https://arxiv.org/abs/1910.02854)/ 可扩展零样本实体链接──
- [De Cao et al. (2020). GENRE](https://arxiv.org/abs/1912.01572)/ 自归实体链接──
