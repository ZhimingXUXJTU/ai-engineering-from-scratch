# Relação Extração e Grafico de Conhecimento Construção de Relações Extração e Grafico de Conhecimento Construção

> A NER encontrou as entidades. A entidade que liga as ancorou. A extração de relações encontra as bordas entre elas. Um gráfico de conhecimento é a soma de nós, bordas e sua proveniência.
> O NER encontrou os elementos. O enlace físico os determinou. A relação extraiu-se para encontrar os lados entre eles.

> **【中文解读】**A partir do texto extrair relações entre os seres, construir um panorama de conhecimento.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 06 (NER), Phase 5 · 25 (Entity Linking) | **前置知识:** Phase 5 · 06（NER），Phase 5 · 25（实体链接）
**Time:** ~60 minutes | **时间:** ~60 分钟

## O problema é o problema da introdução

Relation Extraction (RE) transforma o texto livre em triples estruturados: (subjeto, relação, objeto). "Apple foi fundada por Steve Jobs" → (Apple, fundado por Steve Jobs).

> 关系抽取(RE)将自由文本转化为结构化三元组:(主语, 关系, 宾语) ・・・"A Apple foi fundada por Steve Jobs" → (Apple, fundada por Steve Jobs) ・・・知识图驱动推系统、问答、药物发现和合规监控。

> **【中文解读】**A questão que se coloca neste capítulo é: como entender e aplicar esta técnica na prática da construção.

O problema de 2026: os LLM extraem relações com entusiasmo, mas alucinam bordas que não existem no texto fonte.

> Questão de 2026: LLM 热情地抽取关系但会幻源文本中不存在的边缘―― na construção de gráficos de produção de conhecimento, a precisão é mais importante do que a taxa de recomposição――

## O conceito central.

> **【中文解读】**Este artigo apresenta os conceitos e as bases da teoria.

**Supervised RE.**Treinar um classificador em exemplos de relações rotuladas. Entrada: frase + par de entidades. saída: tipo de relação. Requer dados rotulados.

> **有监督 RE。**Em seu artigo, o artigo 1.o, n.o 1, do artigo 1.o, do Regulamento (UE) n.o 1095/2013 diz que o artigo 1.o, n.o 1, do Regulamento (UE) n.o 1095/2013 é aplicável ao conjunto dos elementos de dados que são utilizados para a elaboração de um documento de identificação.

**Distant supervision.**Alinear texto com triples KB existentes. Se (A, born_in, B) existe no KB, qualquer frase mencionando tanto A quanto B é um exemplo positivo.

> **远程监督。**Se existem no arquivo de conhecimento (A, nascido, B), qualquer frase mencionada em A e B é normal.

**LLM-based RE.**Promover o Mestrado em Direito para extrair relações.

> **基于 LLM 的 RE。**提示 LLM 抽取关系──高召回率,精确率不稳定──需要验证──

> **【拓展：大语言模型的工程实践】**O GPT foi transformado em um campo de discussão.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) é a estrutura mais popular de aplicação de IA em empresas atuais.
```figure
relation-triples
```

## Construí-lo

> **【拓展：NLP 的多语言挑战】**No mundo há mais de 7000 idiomas, mas os estudos de PNL se concentram principalmente em inglês e em uma minoria de línguas.

## Construí-lo e realizei-o.

> **【中文解读】**Este é o capítulo do código do zero implementar o algoritmo central.

```python
def extract_relations(text, entities, llm):
    prompt = f"""Extract all relations between entities from this text.
Text: {text}
Entities: {entities}
Output as JSON list of {{"subject": "...", "relation": "...", "object": "..."}}."""
    return llm(prompt)
```

> **【中文解读】**Este capítulo mostra como usar um quadro de desenvolvimento rápido para aplicar esta tecnologia.

> **【拓展：Prompt Engineering 与 LLM 应用】**A Engenharia Prometida tornou-se a habilidade central de engenheiros de PNL.

## Use-o com o framework implementado.

> **【中文解读】**Este capítulo trata-se de como o modelo será implementado para produtos disponíveis.

- **spaCy + RE models.**O canal de produção para RE. / spaCy + RE 模型──生产 RE 流水线──
- **Hugging Face RE models.**BERT afinado para classificação de relação. / Embracing Face RE 模型。
- **LLM + verification.**Extrair com LLM, verificar contra a fonte. / LLM + 验证。
- **Neo4j.**Armazenar e consultar gráficos de conhecimento. / Neo4j── armazenamento e consulta

## Envia-o . Produto .

Salva como`outputs/skill-re-kg-builder.md`- Não .

> 保存为 `outputs/skill-re-kg-builder.md`- Não .

```markdown
Given a corpus and entity types, build a knowledge graph.
1. RE approach (supervised, distant supervision, LLM).
2. Verification strategy (precision vs recall).
3. KG storage (Neo4j, RDF, property graph).
```

## Exercícios.

1. **Easy.**Extrair relações de 10 frases usando padrões regex. / **简单。**Usar o modelo normal de 10 frases em que se extrai relacionamento.
2. **Medium.**Apontação de um modelo BERT para classificação de relações no TACRED. / **中等。**Em TACRED 上微调 BERT 关系分类模型──
3. **Hard.**Construir um oleoduto completo de KG: NER → EL → RE → Neo4j. / **困难。**Construir KG completo 流水线。

## Termos-chave .

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Relation extraction（关系抽取） | Extract (subject, relation, object) triples from text. / 从文本提取三元组。 |
| Knowledge graph（知识图谱） | Structured graph of entities and relations. / 实体和关系的结构化图。 |
| Distant supervision（远程监督） | Auto-label using existing KB. / 用现有知识库自动标注。 |

## Mais leitura 延伸阅读

- [TACRED](https://nlp.stanford.edu/pubs/tacred17.pdf) relação extração conjunto de dados. / 关系抽取数据集──
- [Neo4j](https://neo4j.com/) base de dados gráfica. / 图数据库。
